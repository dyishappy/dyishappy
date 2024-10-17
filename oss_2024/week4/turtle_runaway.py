import tkinter as tk
import turtle, random

class RunawayGame:
    def __init__(self, root, canvas, runner, chaser, catch_radius=50):
        self.root = root  # Tkinter root 윈도우를 저장
        self.canvas = canvas
        self.runner = runner
        self.chaser = chaser
        self.catch_radius2 = catch_radius**2

        self.score = 20  # 초기 score 값 설정
        self.ai_timer_msec = 100  # 기본 난이도 타이머 설정
        self.game_over = False  # 게임 종료 상태 변수
        self.difficulty_selected = False  # 난이도 선택 여부

        # Initialize 'runner' and 'chaser'
        self.runner.shape('turtle')
        self.runner.color('blue')
        self.runner.penup()

        self.chaser.shape('turtle')
        self.chaser.color('red')
        self.chaser.penup()

        # Instantiate another turtle for drawing
        self.drawer = turtle.RawTurtle(canvas)
        self.drawer.hideturtle()
        self.drawer.penup()

    def is_catched(self):
        p = self.runner.pos()
        q = self.chaser.pos()
        dx, dy = p[0] - q[0], p[1] - q[1]
        return dx**2 + dy**2 < self.catch_radius2

    def start(self, init_dist=400):
        # 난이도 선택 후에만 게임을 시작하게 함
        if not self.difficulty_selected:
            self.show_difficulty_options()
            return

        self.runner.setpos((-init_dist / 2, 0))
        self.runner.setheading(0)
        self.chaser.setpos((+init_dist / 2, 0))
        self.chaser.setheading(180)

        # 시간을 표시하는 Label 생성
        self.after_start_time = 0
        self.time_label = tk.Label(self.root, text=f"Time: {self.after_start_time}s", font=("Arial", 16))
        self.time_label.pack()

        # score 표시를 위한 Label 생성
        self.score_label = tk.Label(self.root, text=f"Enemy's HP: {self.score}", font=("Arial", 16))
        self.score_label.pack()

        # 시간 갱신 함수
        def time_update():
            if not self.game_over:  # 게임이 종료되지 않았을 때만 시간 갱신
                self.after_start_time += 1
                self.time_label.config(text=f"Time: {self.after_start_time}s")
                self.canvas.ontimer(time_update, 1000)

        time_update()
        self.canvas.ontimer(self.step, self.ai_timer_msec)

    def step(self):
        if self.game_over:  # 게임 종료 시 더 이상 업데이트하지 않음
            return

        self.runner.run_ai(self.chaser.pos(), self.chaser.heading())
        self.chaser.run_ai(self.runner.pos(), self.runner.heading())

        is_catched = self.is_catched()
        if is_catched:
            self.score -= 1  # 잡히면 score를 1 줄임
            self.score_label.config(text=f"Enemy's HP: {self.score}")

        # 점수가 0이면 게임 종료
        if self.score <= 0:
            self.game_over = True  # 게임 종료 상태 설정
            self.drawer.undo()
            self.drawer.penup()
            self.drawer.setpos(-300, 300)
            self.drawer.write(f"Clear!", font=("Arial", 30))
            return  # 더 이상 step을 실행하지 않음
        
        if self.after_start_time >= 10:
            self.game_over = True  # 게임 종료 상태 설정
            self.drawer.undo()
            self.drawer.penup()
            self.drawer.setpos(-300, 300)
            self.drawer.write(f"Time Over", font=("Arial", 30))
            
            # 재시작 문구 표시: "Plz"
            self.drawer.setpos(-300,250)  # "Time Over" 메시지 아래에 위치
            self.drawer.write(f"Plz restart game", font=("Arial", 16))  # 추가 문구 출력
            # Restart 버튼 추가
            self.restart_button = tk.Button(self.root, text="Restart", command=self.restart_game)
            self.restart_button.pack()

            return  # 더 이상 step을 실행하지 않음

        # 주기적으로 step 함수 실행
        self.canvas.ontimer(self.step, self.ai_timer_msec)

    def show_difficulty_options(self):
        """난이도 선택 문구 및 버튼 표시"""
        self.drawer.setpos(-150, 0)
        self.drawer.write(f"Choose Difficulty", font=("Arial", 24))

        # 버튼을 사용하여 난이도 선택
        easy_button = tk.Button(self.root, text="Easy", command=lambda: self.set_difficulty(300))
        easy_button.pack()

        medium_button = tk.Button(self.root, text="Medium", command=lambda: self.set_difficulty(150))
        medium_button.pack()

        hard_button = tk.Button(self.root, text="Hard", command=lambda: self.set_difficulty(50))
        hard_button.pack()

        self.difficulty_buttons = [easy_button, medium_button, hard_button]  # 나중에 버튼 제거를 위해 저장

    def set_difficulty(self, timer_value):
        """난이도를 설정하고 게임을 시작"""
        self.ai_timer_msec = timer_value
        self.difficulty_selected = True

        # 버튼 삭제
        for button in self.difficulty_buttons:
            button.pack_forget()

        # 난이도 문구 삭제
        self.drawer.undo()

        # 게임 시작
        self.start()

    def restart_game(self):
        """게임을 재시작하는 함수"""
        # 이전 게임의 요소를 초기화
        self.score = 10
        self.game_over = False

        # 라벨 및 버튼 제거
        self.time_label.pack_forget()
        self.score_label.pack_forget()
        self.restart_button.pack_forget()

        # "Game Over"와 "Plz restart game" 문구 지우기
        self.drawer.clear()  # Turtle 객체에서 그린 텍스트 모두 지우기

        # 새로운 게임 시작
        self.start()

class ManualMover(turtle.RawTurtle):
    def __init__(self, canvas, step_move=10, step_turn=10):
        super().__init__(canvas)
        self.step_move = step_move
        self.step_turn = step_turn

        # Register event handlers
        canvas.onkeypress(lambda: self.forward(self.step_move), 'Up')
        canvas.onkeypress(lambda: self.backward(self.step_move), 'Down')
        canvas.onkeypress(lambda: self.left(self.step_turn), 'Left')
        canvas.onkeypress(lambda: self.right(self.step_turn), 'Right')
        canvas.listen()

    def run_ai(self, opp_pos, opp_heading):
        pass

class RandomMover(turtle.RawTurtle):
    def __init__(self, canvas, difficulty="Medium", step_turn=10):
        super().__init__(canvas)
        self.step_turn = step_turn

         # 난이도에 따라 이동 거리 설정
        if difficulty == 'Easy':
            self.step_move = 10
        elif difficulty == 'Medium':
            self.step_move = 15
        elif difficulty == 'Hard':
            self.step_move = 20

    def run_ai(self, opp_pos, opp_heading):
        mode = random.randint(0, 2)
        if mode == 0:
            self.forward(self.step_move)
        elif mode == 1:
            self.left(self.step_turn)
        elif mode == 2:
            self.right(self.step_turn)

if __name__ == '__main__':
    # Use 'TurtleScreen' instead of 'Screen' to prevent an exception from the singleton 'Screen'
    root = tk.Tk()
    canvas = tk.Canvas(root, width=700, height=700)
    canvas.pack()
    screen = turtle.TurtleScreen(canvas)

    # TODO) Change the follows to your turtle if necessary
    runner = RandomMover(screen)
    chaser = ManualMover(screen)

    game = RunawayGame(root, screen, runner, chaser)
    game.start()
    screen.mainloop()