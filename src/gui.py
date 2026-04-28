import tkinter as tk
from tkinter import messagebox
import engine,os,sys

BG = "#f0f0f0"
BOARD_BG = "#ffffff"
S_COLOR = "#4CAF50"
O_COLOR = "#FF9800"
EMPTY = "#e0e0e0"
TEXT = "#333333"
HEADER = "#2196F3"


def resource_path(relative):
    base = getattr(sys, '_MEIPASS', os.path.dirname(__file__))
    return os.path.join(base, relative)


def set_icon(root):
    try:
        img = tk.PhotoImage(file=resource_path("icon.png"))
        root.iconphoto(True, img)
    except Exception as e:
        print(f"Icon load failed: {e}")



class SOSGameGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("SOS Game")
        self.root.geometry("1200x800")
        self.root.configure(bg=BG)
        
        self.engine = None
        self.board_buttons = []
        self.selected_symbol = tk.StringVar(value="S")
        self.game_active = False
        self.board_size = 5
        self.player_count = 2
        self.mode = 2
        self.active_players = set()
        self.bot_active = False

        self.show_setup()
    
    def show_setup(self):
        """Setup screen with 3 main options"""
        self.clear_window()
        
        title = tk.Label(self.root, text="SOS GAME", font=("Arial", 28, "bold"),
                        bg=HEADER, fg="white")
        title.pack(fill="x", pady=20)
        
        frame = tk.Frame(self.root, bg=BG)
        frame.pack(fill="both", expand=True, padx=40, pady=20)
        
        # Game Mode
        tk.Label(frame, text="Game Mode:", font=("Arial", 14, "bold"), bg=BG).pack(anchor="w", pady=(20, 10))
        mode_var = tk.StringVar(value="2")
        tk.Radiobutton(frame, text="Multiplayer", variable=mode_var, value="2", 
                      font=("Arial", 11), bg=BG).pack(anchor="w")
        tk.Radiobutton(frame, text="vs AI", variable=mode_var, value="1", 
                      font=("Arial", 11), bg=BG).pack(anchor="w")
        
        # Number of Players
        tk.Label(frame, text="Number of Players:", font=("Arial", 14, "bold"), bg=BG).pack(anchor="w", pady=(20, 10))
        player_var = tk.StringVar(value="2")
        tk.Radiobutton(frame, text="2 Players", variable=player_var, value="2", 
                      font=("Arial", 11), bg=BG).pack(anchor="w")
        tk.Radiobutton(frame, text="3 Players", variable=player_var, value="3", 
                      font=("Arial", 11), bg=BG).pack(anchor="w")
        tk.Radiobutton(frame, text="4 Players", variable=player_var, value="4", 
                      font=("Arial", 11), bg=BG).pack(anchor="w")
        
        # Grid Size
        tk.Label(frame, text="Grid Size:", font=("Arial", 14, "bold"), bg=BG).pack(anchor="w", pady=(20, 10))
        size_var = tk.StringVar(value="8")
        for size in ["4", "5", "6", "8"]:
            tk.Radiobutton(frame, text=f"{size}×{size}", variable=size_var, value=size, 
                          font=("Arial", 11), bg=BG).pack(anchor="w")
        
        def start():
            self.mode = int(mode_var.get())
            if self.mode == 1:
                self.player_count = 2  # Force 2 players for AI mode
                self.board_size = int(size_var.get())
                self.engine = engine.GameEngine(self.board_size, self.player_count, self.mode)
                self.active_players = set(range(1, self.player_count + 1))
                self.game_active = True            
                self.show_game()
                return
            self.board_size = int(size_var.get())
            self.player_count = int(player_var.get())
            self.engine = engine.GameEngine(self.board_size, self.player_count, self.mode)
            self.active_players = set(range(1, self.player_count + 1))
            self.game_active = True
            self.show_game()
        
        tk.Button(frame, text="START GAME", command=start, font=("Arial", 12, "bold"),
                 bg=HEADER, fg="white", padx=20, pady=10).pack(pady=(30, 10))
        tk.Button(frame, text="EXIT", command=self.root.quit, font=("Arial", 11),
                 bg="#999", fg="white", padx=20, pady=8).pack()
    
    def show_game(self):
        """Main game screen"""
        self.clear_window()
        
        top_frame = tk.Frame(self.root, bg=HEADER)
        top_frame.pack(fill="x")
        
        self.score_label = tk.Label(top_frame, text="", font=("Arial", 12, "bold"),
                                   bg=HEADER, fg="white")
        self.score_label.pack(pady=10)
        
        mid_frame = tk.Frame(self.root, bg=BG)
        mid_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        board_frame = tk.Frame(mid_frame, bg=BOARD_BG, bd=2, relief="solid")
        board_frame.pack(side="left")
        
        self.board_buttons = []
        for i in range(self.board_size):
            row = []
            for j in range(self.board_size):
                btn = tk.Button(board_frame, text="", width=6, height=3,
                               font=("Arial", 14, "bold"), bg=EMPTY,
                               command=lambda r=i, c=j: self.on_click(r, c))
                btn.grid(row=i, column=j, padx=2, pady=2)
                row.append(btn)
            self.board_buttons.append(row)
        
        ctrl_frame = tk.Frame(mid_frame, bg=BG)
        ctrl_frame.pack(side="right", fill="y", padx=(20, 0))
        
        tk.Label(ctrl_frame, text="Choose Symbol:", font=("Arial", 11, "bold"), bg=BG).pack(anchor="w", pady=(0, 10))
        tk.Radiobutton(ctrl_frame, text="S", variable=self.selected_symbol, value="S",
                      font=("Arial", 12), bg=BG, fg=S_COLOR).pack(anchor="w")
        tk.Radiobutton(ctrl_frame, text="O", variable=self.selected_symbol, value="O",
                      font=("Arial", 12), bg=BG, fg=O_COLOR).pack(anchor="w")
        
        tk.Button(ctrl_frame, text="New Game", command=self.show_setup, font=("Arial", 10),
                 bg="#4CAF50", fg="white", width=12).pack(pady=(20, 10))
        tk.Button(ctrl_frame, text="Quit Game", command=self.quit_player, font=("Arial", 10),
                 bg="#f44336", fg="white", width=12).pack()
        
        bottom_frame = tk.Frame(self.root, bg=HEADER)
        bottom_frame.pack(fill="x")
        
        self.player_label = tk.Label(bottom_frame, text="", font=("Arial", 12, "bold"),
                                    bg=HEADER, fg="white")
        self.player_label.pack(pady=10)
        
        self.update_board()
        self.update_info()
    
    def on_click(self, row, col):
        """Handle cell click"""
        if not self.game_active:
            return
        
        if self.bot_active:
           messagebox.showinfo("Wait", "Please wait for the bot to finish its turn.")
           return
        

        current_player = self.engine.getCurrentPlayer()
        if current_player not in self.active_players:
            return
        
        if self.engine.getBoardCell(row, col) != "-":
            messagebox.showwarning("Invalid", "Cell already occupied!")
            return
        
        symbol = self.selected_symbol.get()
        success, scored = self.engine.makeMove(row, col, symbol)
        
        if not success:
            messagebox.showerror("Error", "Invalid move!")
            return
        
        self.update_board()
        self.update_info()
        
        if self.engine.gameOverCheck():
            self.game_over()
            return
        
        if not scored:
            # Turn passed to next player, skip if inactive
            self.advance_to_next_active_player_after_move()
    
    def advance_to_next_active_player_after_move(self):
        """After a move, skip inactive players and continue game"""
        for _ in range(self.player_count):
            next_player = self.engine.getCurrentPlayer()
            if next_player in self.active_players:
                self.update_info()
                # If AI and active, make move
                if self.mode == 1 and next_player == 2 and next_player in self.active_players:
                    self.root.after(500, self.bot_move)
                return
            
            # Current player is inactive, advance to next
            self.engine.updateCurrentPlayer("playerQuit")
        
        self.update_info()
    
    def bot_move(self):
        """Bot's move"""
        if not self.game_active:
            return
        
        current_player = self.engine.getCurrentPlayer()
        if current_player not in self.active_players:
            return
        
        move = self.engine.getBotMove()
        if move[0] is None:
            return
        
        i, j, symb = move
        success, scored = self.engine.makeMove(i, j, symb)
        
        if success:
            self.update_board()
            self.update_info()
            
            if self.engine.gameOverCheck():
                self.game_over()
                return
            
            if scored:
                # Bot scored, gets another turn
                self.root.after(500, self.bot_move)
                self.bot_active=True
            else:
                # Turn passed, skip to next active player if needed
                self.bot_active=False
                self.root.after(500, self.advance_to_next_active_player_after_move)
    
    def update_board(self):
        """Update board display"""
        for i in range(self.board_size):
            for j in range(self.board_size):
                cell = self.engine.getBoardCell(i, j)
                if cell == "S":
                    self.board_buttons[i][j].config(text="S", bg=S_COLOR, fg="white")
                elif cell == "O":
                    self.board_buttons[i][j].config(text="O", bg=O_COLOR, fg="white")
                else:
                    self.board_buttons[i][j].config(text="", bg=EMPTY, fg=TEXT)
    
    def update_info(self):
        """Update scores and player info"""
        scores = self.engine.getPlayerScores()
        current = self.engine.getCurrentPlayer()
        
        score_text = " | ".join([f"P{i+1}: {scores[i]}" for i in range(self.player_count)])
        self.score_label.config(text=score_text)
        
        active_status = " | ".join([f"P{i+1}: {'IN' if i+1 in self.active_players else 'OUT'}" for i in range(self.player_count)])
        player_text = f"Current Player: {current} | {active_status}"
        self.player_label.config(text=player_text)
    
    def game_over(self):
        """Game over popup"""
        self.game_active = False
        scores = self.engine.getFinalScores()
        winner = scores.index(max(scores)) + 1
        
        msg = "GAME OVER!\n\n"
        for i, score in enumerate(scores):
            msg += f"Player {i+1}: {score}\n"
        msg += f"\nPlayer {winner} Wins!"
        
        messagebox.showinfo("Game Over", msg)
        self.show_setup()
    
    def quit_player(self):
        """Handle individual player quitting"""
        current_player = self.engine.getCurrentPlayer()
        
        if messagebox.askokcancel("Quit Game", f"Player {current_player}, are you sure you want to quit?"):
            self.active_players.discard(current_player)
            
            # Update engine about quitting player
            self.engine.updateQuittingPlayerScore(current_player - 1)
            
            if len(self.active_players) == 0:
                # All players have quit
                self.game_active = False
                msg = "GAME ENDED! All players have quit.\n\n"
                scores = self.engine.getFinalScores()
                for i, score in enumerate(scores):
                    msg += f"Player {i+1}: {score}\n"
                
                messagebox.showinfo("Game Ended", msg)
                self.show_setup()
                return
            
            if len(self.active_players) == 1:
                # Only one player left
                self.game_active = False
                remaining = list(self.active_players)[0]
                
                msg = "GAME ENDED!\n\n"
                scores = self.engine.getFinalScores()
                for i, score in enumerate(scores):
                    status = "QUIT" if i + 1 not in self.active_players else "WINNER"
                    msg += f"Player {i+1}: {score} ({status})\n"
                
                msg += f"\nPlayer {remaining} is the last remaining player!"
                
                messagebox.showinfo("Game Ended", msg)
                self.show_setup()
                return
            
            # Continue with next active player
            messagebox.showinfo("Player Quit", f"Player {current_player} has quit!\nContinuing with remaining players...")
            
            # Advance to next player and skip inactive ones
            self.advance_to_next_active_player()
    
    def advance_to_next_active_player(self):
        """Skip turns until we find an active player"""
        self.update_info()
        
        # Check if we need to skip to the next active player
        for _ in range(self.player_count):
            next_player = self.engine.getCurrentPlayer()
            if next_player in self.active_players:
                self.update_info()
                # If AI and active, make move
                if self.mode == 1 and next_player == 2 and next_player in self.active_players:
                    self.root.after(500, self.bot_move)
                return
            
            # Current player is inactive, advance to next
            self.engine.updateCurrentPlayer("playerQuit")
        
        self.update_info()
    
    def clear_window(self):
        """Clear all widgets"""
        for widget in self.root.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    set_icon(root)
    gui = SOSGameGUI(root)
    root.mainloop()
