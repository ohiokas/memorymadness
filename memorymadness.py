import pygame
import random
import time
import string

# Inisialisasi pygame
pygame.init()

# Konstanta layar
WIDTH, HEIGHT = 800, 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
LIGHT_BLUE = (173, 216, 230)
DARK_BLUE = (70, 130, 180)

# Font dan ukuran (diperkecil)
FONT = pygame.font.Font(None, 50)  # Font untuk teks besar
SMALL_FONT = pygame.font.Font(None, 30)  # Font untuk teks kecil
TITLE_FONT = pygame.font.Font(None, 60)  # Font untuk judul

# Membuat layar
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Memory Madness")

# Warna dan lainnya
correct_color = GREEN
incorrect_color = RED
input_color = BLACK
background_color = LIGHT_BLUE


# Kelas dasar Screen yang akan digunakan untuk kelas turunan
# Encapsulation: Menyembunyikan atribut terkait tampilan (screen, drawing, etc.)
class Screen:
    def __init__(self):
        self.running = True

    # Metode untuk menggambar tombol dengan teks
    def draw_button(self, text, x, y, width, height, color, text_color):
        pygame.draw.rect(screen, color, (x, y, width, height))
        text_surface = SMALL_FONT.render(text, True, text_color)  # Menggunakan SMALL_FONT yang lebih kecil
        text_rect = text_surface.get_rect(center=(x + width // 2, y + height // 2))
        screen.blit(text_surface, text_rect)

    # Menampilkan teks pada posisi tertentu
    def display_text(self, text, font, color, y_offset=0):
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2 + y_offset))
        screen.blit(text_surface, text_rect)

    # Event handler untuk menunggu input atau keluar
    def wait_for_event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                return


# Kelas Game yang mewarisi kelas Screen
# Inheritance: Kelas Game mewarisi atribut dan metode dari Screen, sehingga kita tidak perlu menulis ulang kode yang sama.
class Game(Screen):
    def __init__(self):
        super().__init__()  # Memanggil konstruktor kelas Screen
        self.score = 0
        self.level = 1
        self.correct_answers = 0
        self.user_input = ""
        self.letters_to_remember = []
        self.incorrect_count = 0
        self.questions_answered = 0
        self.game_over = False

    # Metode untuk menghasilkan karakter acak
    def generate_random_characters(self, num_characters):
        if self.level >= 3 and self.level < 5:
            characters = string.ascii_uppercase + string.digits
        elif self.level >= 5:
            characters = string.ascii_uppercase + string.digits + string.punctuation
        else:
            characters = string.ascii_uppercase
        
        return ''.join(random.choice(characters) for _ in range(num_characters))

    # Menentukan kategori memori berdasarkan skor
    def determine_memory_category(self, score):
        if score >= 195 and score <= 210:
            return "Are You A Human?"
        elif score >= 175 and score < 195:
            return "Jenius"
        elif score >= 155 and score < 175:
            return "Superior"
        elif score >= 135 and score < 155:
            return "Good"
        elif score >= 120 and score < 135:
            return "Medium"
        elif score >= 80 and score < 120:
            return "Not Bad"
        elif score >= 30 and score < 75:
            return "BAD"
        else:
            return "Spechless"

    def game_loop(self):
        clock = pygame.time.Clock()
        self.letters_to_remember = self.generate_random_characters(self.level + 4)
        self.user_input = ""

        display_time = 2
        start_time = time.time()

        while time.time() - start_time < display_time:
            screen.fill(background_color)
            self.display_text(self.letters_to_remember, FONT, BLACK)
            pygame.display.flip()
            clock.tick(60)

        input_prompt = SMALL_FONT.render("Masukkan urutan karakter:", True, input_color)
        screen.fill(background_color)
        screen.blit(input_prompt, (50, 100))
        pygame.display.flip()

        self.user_input = ""
        waiting_for_input = True
        while waiting_for_input:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    return
        waiting_for_restart = True
        while waiting_for_restart:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return

                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    if WIDTH // 2 - 160 < mouse_x < WIDTH // 2 - 40 and HEIGHT - 100 < mouse_y < HEIGHT - 60:
                        self.restart_game()
                    elif WIDTH // 2 + 40 < mouse_x < WIDTH // 2 + 160 and HEIGHT - 100 < mouse_y < HEIGHT - 60:
                        pygame.quit()
                        return

    # Restart game dan reset semuanya
    def restart_game(self):
        self.score = 0
        self.level = 1
        self.correct_answers = 0
        self.user_input = ""
        self.incorrect_count = 0
        self.questions_answered = 0
        self.game_loop()

    # Tampilan awal untuk memulai permainan
    def start_screen(self):
        while self.running:
            screen.fill(background_color)
            title_text = TITLE_FONT.render("Memory Madness", True, DARK_BLUE)
            screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, HEIGHT // 3))

            self.draw_button("Start", WIDTH // 2 - 80, HEIGHT // 2 + 50, 160, 40, DARK_BLUE, (0, 0, 100))  # Ukuran tombol lebih kecil

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return

                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    if WIDTH // 2 - 80 < mouse_x < WIDTH // 2 + 80 and HEIGHT // 2 + 50 < mouse_y < HEIGHT // 2 + 90:
                        self.game_loop()

# Main function untuk memulai permainan
if __name__ == "__main__":
    game = Game()
    game.start_screen()
    pygame.quit()
