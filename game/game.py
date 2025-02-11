# -*- coding: utf-8 -*-
# Kullanılan modüller: Pygame Zero (Actor, keyboard, keys, screen, music vs.), math, random ve pygame’den yalnızca Rect.
import random
from math import sqrt
from pygame import Rect  # İzin verilen tek pygame modülü

# Ekran boyutları
WIDTH = 1200
HEIGHT = 800

# Global oyun durumu: "menu", "game", "win"
game_state = "menu"
sound_on = True  # Ses/müzik durumu
menu_music_playing = False  # Menü müziğinin çalıp çalmadığını takip eder
hero_health = 20  # Ana karakterin canı (örnek başlangıç değeri)

# Level bilgileri
level = 1
max_level = 5
# Level çarpanı: her levelde tüm karakterlerin hızı, 1.1^(level-1) katına çıkar.
def level_multiplier():
    return 1.1 ** (level - 1)

# Global referanslar (oyuncu, düşman listesi, duvar listesi, bıçak listesi)
hero = None
enemies = []
walls = []
knives = []  # Fırlatılan bıçaklar

# Eskiden exit alanı kullanılıyordu; artık seviye geçişi düşmanların tamamının ölmesiyle sağlanıyor.
exit_area = Rect((WIDTH - 100, HEIGHT - 100), (80, 80))

# -------------------------------------------------------------------
# Sınıflar
# -------------------------------------------------------------------
class Hero:
    def __init__(self):
        self.health = 20
        self.base_speed = 5
        self.power = 2
        self.pos = [100, 100]
        # Hız level çarpanı ile artar:
        self.speed = self.base_speed * level_multiplier()
        # Eğer animasyon için birden fazla kare varsa; yoksa aynı görsel kullanılır.
        self.frames = ["anakarakter"]  # assets/images/anakarakter.png
        self.current_frame = 0
        self.frame_timer = 0
        self.actor = Actor(self.frames[self.current_frame], pos=self.pos)
        self.direction = (1, 0)  # Varsayılan yön sağa

    def update(self):
        # Hareket kontrolü
        old_pos = self.pos[:]
        dx, dy = 0, 0
        if keyboard.left:
            dx -= self.speed
        if keyboard.right:
            dx += self.speed
        if keyboard.up:
            dy -= self.speed
        if keyboard.down:
            dy += self.speed

        # Eğer hareket varsa, yönü güncelle (normalized)
        if dx != 0 or dy != 0:
            mag = sqrt(dx*dx + dy*dy)
            self.direction = (dx/mag, dy/mag)

        self.pos[0] += dx
        self.pos[1] += dy
        self.actor.pos = self.pos

        self.pos[0] = max(0, min(WIDTH, self.pos[0]))
        self.pos[1] = max(0, min(HEIGHT, self.pos[1]))
        self.actor.pos = self.pos

    def draw(self):
        self.actor.draw()

class Enemy:
    def __init__(self, enemy_type, start_pos):
        self.type = enemy_type
        # Türüne göre özellikler:
        if enemy_type == "hayalet":
            self.health = 6
            self.base_speed = 1
            self.power = 3
            self.frames = ["enemy/hayalet"]
        elif enemy_type == "orumcek":
            self.health = 4
            self.base_speed = 2
            self.power = 2
            self.frames = ["enemy/orumcek"]
        elif enemy_type == "batman":
            self.health = 2
            self.base_speed = 4
            self.power = 1
            self.frames = ["enemy/batman"]
        # Hız level çarpanı ile artar; düşmanların hızı her zaman ana karakterden (base_speed:5) düşük olmalı
        self.speed = self.base_speed * level_multiplier()
        self.pos = start_pos[:]  # Liste kopyası
        self.actor = Actor(self.frames[0], pos=self.pos)
        self.current_frame = 0
        self.frame_timer = 0
        self.collision_cooldown = 0  # Çarpışma sonrası hasar uygulanmaması için

    def update(self):
        # Ana karaktere doğru hareket
        dx = hero.pos[0] - self.pos[0]
        dy = hero.pos[1] - self.pos[1]
        dist = sqrt(dx*dx + dy*dy)
        if dist != 0:
            dx, dy = dx/dist, dy/dist
        # Esnek hareket: speed * yön vektörü
        new_x = self.pos[0] + dx * self.speed
        new_y = self.pos[1] + dy * self.speed
        old_pos = self.pos[:]
        self.pos = [new_x, new_y]
        self.actor.pos = self.pos

        # Duvar çarpışması: Eğer düşman herhangi bir duvara dokunursa, rastgele bir konuma ışınlanır.
        for wall in walls:
            if self.actor.colliderect(wall.actor):
                self.pos = [random.randint(0, WIDTH), random.randint(0, HEIGHT)]
                self.actor.pos = self.pos
                break

        # Çarpışma sonrası koruma süresi (cooldown)
        if self.collision_cooldown > 0:
            self.collision_cooldown -= 1

        self.pos[0] = max(0, min(WIDTH, self.pos[0]))
        self.pos[1] = max(0, min(HEIGHT, self.pos[1]))
        self.actor.pos = self.pos

        # Basit animasyon (frame her 15 frame'de değişir)
        self.frame_timer += 1
        if self.frame_timer > 15:
            self.frame_timer = 0
            self.current_frame = (self.current_frame + 1) % len(self.frames)
            self.actor.image = self.frames[self.current_frame]

    def draw(self):
        self.actor.draw()

class Wall:
    def __init__(self, pos):
        self.pos = pos
        self.actor = Actor("duvar", pos=self.pos)

    def draw(self):
        self.actor.draw()

class Knife:
    def __init__(self, pos, direction):
        self.pos = pos[:]  # Başlangıç pozisyonu
        self.direction = direction  # Normalleştirilmiş yön (tuple)
        self.speed = 10  # Bıçak hızı
        self.actor = Actor("bicak", pos=self.pos)  # assets/images/bicak.png
        self.distance_travelled = 0
        self.max_distance = 400  # Maksimum yolculuk mesafesi

    def update(self):
        self.pos[0] += self.direction[0] * self.speed
        self.pos[1] += self.direction[1] * self.speed
        self.distance_travelled += self.speed
        self.actor.pos = self.pos

    def draw(self):
        self.actor.draw()

# -------------------------------------------------------------------
# Level ve Oyun Kurulum Fonksiyonları
# -------------------------------------------------------------------
def setup_level():
    global hero, enemies, walls, knives
    knives.clear()
    multiplier = level_multiplier()
    if hero is None:
        # Yeni oyunda hero oluşturulurken can 20 olur.
        hero = Hero()
    else:
        # Yeni levela geçerken; konum, hız vs. güncelleniyor fakat hero.health reset edilmiyor.
        hero.pos = [100, 100]
        hero.actor.pos = hero.pos
        hero.speed = hero.base_speed * multiplier
        # hero.health satırı kaldırıldı; böylece önceki levelden kalan can korunur.
    enemies.clear()
    # Her level için her düşman türünden "level" adet oluştur
    for i in range(level):
        enemies.append(Enemy("hayalet", [WIDTH - 200, 100 + i*50]))
        enemies.append(Enemy("orumcek", [WIDTH - 200, HEIGHT - 200 - i*50]))
        enemies.append(Enemy("batman", [100, HEIGHT - 200 - i*50]))
    for enemy in enemies:
        enemy.speed = enemy.base_speed * multiplier
    walls.clear()
    walls.append(Wall((WIDTH//2, HEIGHT//2)))
    walls.append(Wall((WIDTH//2 - 150, HEIGHT//2)))
    walls.append(Wall((WIDTH//2 + 150, HEIGHT//2)))

# -------------------------------------------------------------------
# Pygame Zero Fonksiyonları
# -------------------------------------------------------------------
def update():
    global game_state, level, hero_health, menu_music_playing
    if game_state == "game":
        hero.update()
        for enemy in enemies[:]:
            enemy.update()
        for knife in knives[:]:
            knife.update()
            # Bıçak ile düşman çarpışması kontrolü
            for enemy in enemies[:]:
                if knife.actor.colliderect(enemy.actor):
                    enemy.health -= hero.power
                    if enemy.health <= 0:
                        enemies.remove(enemy)
                        sounds.dusmanoldu.play()  # Düşman öldüğünde tek seferlik ses
                    if knife in knives:
                        knives.remove(knife)
                    break
            if knife.distance_travelled >= knife.max_distance:
                if knife in knives:
                    knives.remove(knife)
        # Ana karakter ile düşman çarpışması kontrolü
        for enemy in enemies[:]:
            if hero.actor.colliderect(enemy.actor) and enemy.collision_cooldown == 0:
                hero.health -= enemy.power
                sounds.canazal.play()  # Can azaldığında tek seferlik ses
                enemy.health -= hero.power
                enemy.collision_cooldown = 20  # Yaklaşık 20 frame koruma süresi
                if enemy.health <= 0:
                    enemies.remove(enemy)
                    sounds.dusmanoldu.play()  # Düşman öldüğünde tek seferlik ses
                if hero.health <= 0:
                    game_state = "menu"
                    reset_game()
        # Eğer tüm düşmanlar öldüyse seviye geçişi
        if not enemies:
            level += 1
            if level > max_level:
                game_state = "win"
            else:
                setup_level()
        hero_health = hero.health
    elif game_state == "menu":
        if hero_health <= 0:
            game_state = "menu"
        if game_state == "menu" and sound_on and not menu_music_playing:
            music.play("music1.wav")
            menu_music_playing = True
        elif (game_state != "menu" or not sound_on) and menu_music_playing:
            music.stop()
            menu_music_playing = False
    elif game_state == "win":
        pass

def draw():
    if game_state == "game":
        screen.clear()
        # Duvarları çiz
        for wall in walls:
            wall.draw()
        # Ana karakteri, düşmanları ve fırlatılan bıçakları çiz
        hero.draw()
        for enemy in enemies:
            enemy.draw()
        for knife in knives:
            knife.draw()
        # Sağ üstte ana karakterin canını göster
        screen.draw.text("Health: " + str(hero.health), topleft=(10, 10), fontsize=40, color="red")
        # Sol üstte level bilgisini göster
        screen.draw.text("Level: " + str(level), topright=(WIDTH - 10, 10), fontsize=40, color="white")
    elif game_state == "menu":
        screen.clear()
        # Menü ekranı
        screen.draw.text("Main Menu", center=(WIDTH // 2, 100), fontsize=60, color="yellow")
        screen.draw.text("Play Game", center=(WIDTH // 2, 250), fontsize=50, color="white")
        screen.draw.text("Sound On/Off", center=(WIDTH // 2, 350), fontsize=50, color="white")
        screen.draw.text("Exit", center=(WIDTH // 2, 450), fontsize=50, color="white")
    elif game_state == "win":
        screen.clear()
        screen.draw.text("You Win!", center=(WIDTH//2, HEIGHT//2), fontsize=70, color="green")
        screen.draw.text("Press SPACE to Return to Menu", center=(WIDTH//2, HEIGHT//2+80), fontsize=40, color="white")

def on_mouse_down(pos):
    global game_state, sound_on, menu_music_playing
    if game_state == "menu":
        if (WIDTH // 2 - 150 < pos[0] < WIDTH // 2 + 150) and (250 - 30 < pos[1] < 250 + 30):
            setup_level()
            music.stop()  # Menü müziğini durdur
            music.play("music2.wav")  # Oyun müziğini sürekli çalacak şekilde başlat
            game_state = "game"
        elif (WIDTH // 2 - 200 < pos[0] < WIDTH // 2 + 200) and (350 - 30 < pos[1] < 350 + 30):
            sound_on = not sound_on
            if sound_on:
                music.play("music1.wav")
                menu_music_playing = True
            else:
                music.stop()
                menu_music_playing = False
        elif (WIDTH // 2 - 100 < pos[0] < WIDTH // 2 + 100) and (450 - 30 < pos[1] < 450 + 30):
            exit()

def on_key_down(key):
    global game_state, level
    if game_state in ["menu", "win"]:
        if key == keys.SPACE:
            level = 1
            setup_level()
            game_state = "menu"
    elif game_state == "game":
        # "Enter" tuşu ile bıçağı fırlat
        if key == keys.RETURN:
            sounds.bicak.play()  # Bıçak fırlatıldığında tek seferlik ses
            knife = Knife(hero.pos, hero.direction)
            knives.append(knife)

def reset_game():
    """Ana karakter ölünce oyunu başa döndürür."""
    global level, hero
    level = 1
    hero = None
    setup_level()

# -------------------------------------------------------------------
# Başlangıç Ayarı: Oyuna girmeden önce ana menüde bekleyelim.
# -------------------------------------------------------------------
# Oyunu çalıştırmadan önce game_state "menu" olarak kalır.
