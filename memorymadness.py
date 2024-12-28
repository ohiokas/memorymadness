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
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        if self.user_input == self.letters_to_remember:
                            self.correct_answers += 1
                            self.score += 10
                            self.questions_answered += 1
                            if self.correct_answers % 5 == 0:
                                self.level += 1
                        else:
                            self.incorrect_count += 1
                            self.score -= 5
                            self.questions_answered += 1
                        waiting_for_input = False

                    elif event.key == pygame.K_BACKSPACE:
                        self.user_input = self.user_input[:-1]

                    elif len(self.user_input) < len(self.letters_to_remember):
                        self.user_input += event.unicode.upper()

            screen.fill(background_color)
            self.display_text(self.user_input, FONT, input_color, y_offset=100)
            pygame.display.flip()
            clock.tick(60)

        screen.fill(background_color)
        if self.user_input == self.letters_to_remember:
            feedback_text = SMALL_FONT.render("Correct! +10 points", True, correct_color)
        else:
            feedback_text = SMALL_FONT.render("Incorrect! -5 points", True, incorrect_color)

        score_text = SMALL_FONT.render(f"Score: {self.score}", True, BLACK)
        level_text = SMALL_FONT.render(f"Level: {self.level}", True, BLACK)
        questions_text = SMALL_FONT.render(f"Questions Answered: {self.questions_answered}", True, BLACK)
        screen.blit(feedback_text, (WIDTH // 2 - feedback_text.get_width() // 2, HEIGHT // 2 + 50))
        screen.blit(score_text, (50, 50))
        screen.blit(level_text, (WIDTH - level_text.get_width() - 50, 50))
        screen.blit(questions_text, (WIDTH // 2 - questions_text.get_width() // 2, HEIGHT - 150))

        pygame.display.flip()

         if self.incorrect_count >= 3:
            self.game_over_screen()

        pygame.time.delay(1000)
        if self.running and self.incorrect_count < 3:
            self.game_loop()

    def game_over_screen(self):
        screen.fill(background_color)
        game_over_text = TITLE_FONT.render("Game Over!", True, RED)
        score_text = FONT.render(f"Your Score: {self.score}", True, BLACK)
        questions_text = FONT.render(f"Questions Answered: {self.questions_answered}", True, BLACK)

        memory_category = self.determine_memory_category(self.score)
        memory_text = FONT.render(f"YOUR MEMORY: {memory_category}", True, BLACK)

        screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 3))
        screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, HEIGHT // 2))
        screen.blit(questions_text, (WIDTH // 2 - questions_text.get_width() // 2, HEIGHT // 2 + 60))
        screen.blit(memory_text, (WIDTH // 2 - memory_text.get_width() // 2, HEIGHT // 2 + 120))

        self.draw_button("Leaderboard", WIDTH // 2 - 80, HEIGHT - 100, 160, 40, DARK_BLUE, (0, 0, 100))
        self.draw_button("Restart", WIDTH // 2 - 160, HEIGHT - 50, 120, 40, DARK_BLUE, (0, 0, 100))
        self.draw_button("Exit", WIDTH // 2 + 40, HEIGHT - 50, 120, 40, DARK_BLUE, (0, 0, 100))

        pygame.display.flip()
        
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
