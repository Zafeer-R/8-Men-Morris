import tkinter as tk
from tkinter import messagebox
import os

class GridPatternGUI:
    def __init__(self, root, filename, window_title=None):
        self.root = root
        self.filename = filename
        
        # Set window title based on filename if not provided
        if window_title:
            self.root.title(window_title)
        else:
            self.root.title(f"Grid Pattern Viewer - {filename}")
        
        self.root.geometry("800x700")
        self.root.minsize(600, 500)  # Set minimum window size
        
        # Define the mapping from string index to grid position (row, col)
        # Based on three concentric boxes: 11x11, 7x7, 3x3
        self.index_to_position = {
            # Outermost box (11x11 border) - positions: 0,1,20,19,18,6
            0: (10, 0),  # Bottom left corner
            1: (10, 10), # Bottom right corner
            11: (5,10),
            20: (0, 10), # Top right corner
            19: (0, 5),  # Top center
            18: (0, 0),  # Top left corner
            6: (5, 0),   # Left middle
            
            # Middle box (7x7 border) - positions: 2,3,10,17,16,15,7
            2: (8, 2),   # Bottom left of middle box
            3: (8, 8),   # Bottom right of middle box
            10: (5, 8),  # Top right of middle box
            17: (2, 8),  # Top right inner of middle box
            16: (2, 5),  # Top left inner of middle box
            15: (2, 2),  # Top left of middle box
            7: (5, 2),   # Left side of middle box
            
            # Innermost box (3x3) - positions: 4,5,9,14,13,12,8
            4: (6, 4),   # Bottom left of inner box
            5: (6, 6),   # Bottom right of inner box
            14: (4, 6),   # Top right of inner box
            8: (5, 4),  # Top left of inner box
            13: (4, 5),  # Top center of inner box
            12: (4, 4),  # Left center of inner box
            9: (5, 6),   # Center of inner box
        }
        
        # Grid dimensions for 11x11
        self.grid_rows = 11
        self.grid_cols = 11
        
        # Create the GUI
        self.setup_gui()
        
        # Auto-load the file on startup
        self.load_file()
        
    def setup_gui(self):
        # Create main frame
        main_frame = tk.Frame(self.root)
        main_frame.pack(padx=20, pady=20, fill=tk.BOTH, expand=True)
        
        # File info and refresh frame
        file_frame = tk.Frame(main_frame)
        file_frame.pack(pady=(0, 20))
        
        tk.Label(file_frame, text="File:", font=("Arial", 12, "bold")).pack(side=tk.LEFT, padx=(0, 10))
        
        self.file_label = tk.Label(file_frame, text=self.filename, 
                                  font=("Arial", 12), fg="blue")
        self.file_label.pack(side=tk.LEFT, padx=(0, 20))
        
        # Add refresh button
        refresh_button = tk.Button(file_frame, text="Refresh", 
                                 command=self.refresh_file, 
                                 font=("Arial", 10),
                                 bg="lightblue", 
                                 relief=tk.RAISED,
                                 padx=10)
        refresh_button.pack(side=tk.LEFT)
        
        # Grid frame with 11x11 layout - make it expandable
        self.grid_frame = tk.Frame(main_frame, bg="darkgray", relief=tk.RAISED, bd=3)
        self.grid_frame.pack(pady=10, padx=20, fill=tk.BOTH, expand=True)
        
        # Configure grid frame to expand properly
        for i in range(self.grid_rows):
            self.grid_frame.grid_rowconfigure(i, weight=1)
        for j in range(self.grid_cols):
            self.grid_frame.grid_columnconfigure(j, weight=1)
        
        # Create 11x11 grid cells with relative sizing
        self.cells = {}
        
        for row in range(self.grid_rows):
            for col in range(self.grid_cols):
                # Determine if this cell is part of the pattern
                is_outer_border = (row == 0 or row == 10 or col == 0 or col == 10)
                is_middle_border = ((row == 2 or row == 8) and 2 <= col <= 8) or \
                                 ((col == 2 or col == 8) and 2 <= row <= 8)
                is_inner_area = (4 <= row <= 6 and 4 <= col <= 6)
                
                if is_outer_border or is_middle_border or is_inner_area:
                    # Active pattern cell - no fixed width/height
                    cell = tk.Label(self.grid_frame, 
                                  relief=tk.FLAT, bd=1,
                                  bg="lightgray", fg="black",
                                  font=("Arial", 8, "bold"))
                else:
                    # Empty space cell - no fixed width/height
                    cell = tk.Label(self.grid_frame, 
                                  relief=tk.FLAT, bd=0,
                                  bg="white", fg="white")
                
                # Use sticky to make cells expand to fill their grid space
                cell.grid(row=row, column=col, padx=1, pady=1, sticky="nsew")
                self.cells[(row, col)] = cell
        
        # Status frame
        status_frame = tk.Frame(main_frame)
        status_frame.pack(pady=(20, 0), fill=tk.X)
        
        self.status_label = tk.Label(status_frame, 
                                   text="Loading pattern...", 
                                   font=("Arial", 10))
        self.status_label.pack()
        
        # Legend
        legend_frame = tk.Frame(main_frame)
        legend_frame.pack(pady=(10, 0))
        
        tk.Label(legend_frame, text="Legend:", font=("Arial", 10, "bold")).pack()
        legend_row = tk.Frame(legend_frame)
        legend_row.pack()
        
        # Legend items
        legends = [("W", "white", "W - White"),
                  ("B", "black", "B - Black"), 
                  ("x", "red", "x - Empty/Special")]
        
        for char, color, desc in legends:
            frame = tk.Frame(legend_row)
            frame.pack(side=tk.LEFT, padx=10)
            
            sample = tk.Label(frame, text=char, bg=color, 
                            fg="white" if color == "black" else "black",
                            width=3, height=1, relief=tk.RAISED, bd=1)
            sample.pack()
            tk.Label(frame, text=desc, font=("Arial", 8)).pack()
    
    def refresh_file(self):
        """Refresh button callback - reloads the file and updates display"""
        self.status_label.config(text="Refreshing...", fg="blue")
        self.root.update()  # Force GUI update to show "Refreshing..." message
        self.load_file()
    
    def load_file(self):
        try:
            if not os.path.exists(self.filename):
                self.status_label.config(text=f"Error: File '{self.filename}' not found", fg="red")
                return
                
            with open(self.filename, 'r') as file:
                content = file.read().strip()
            
            if len(content) != 21:
                self.status_label.config(text=f"Error: File must contain 21 characters, found {len(content)}", fg="red")
                return
            
            # Validate characters
            valid_chars = {'W', 'B', 'x'}
            invalid_chars = set(content) - valid_chars
            if invalid_chars:
                self.status_label.config(text=f"Error: Invalid characters: {invalid_chars}", fg="red")
                return
            
            self.display_pattern(content)
            self.status_label.config(text=f"Pattern loaded successfully: {content}", fg="green")
            
        except Exception as e:
            self.status_label.config(text=f"Error reading '{self.filename}': {str(e)}", fg="red")
    
    def display_pattern(self, pattern_string):
        # Reset all cells first - clear everything completely
        for row in range(self.grid_rows):
            for col in range(self.grid_cols):
                cell = self.cells[(row, col)]
                
                # Determine cell type and set default appearance
                is_outer_border = (row == 0 or row == 10 or col == 0 or col == 10)
                is_middle_border = ((row == 2 or row == 8) and 2 <= col <= 8) or \
                                 ((col == 2 or col == 8) and 2 <= row <= 8)
                is_inner_area = (4 <= row <= 6 and 4 <= col <= 6)
                
                if is_outer_border or is_middle_border or is_inner_area:
                    # Reset active pattern cells to default state
                    cell.config(bg="lightgray", text="", relief=tk.FLAT, bd=1, fg="black")
                else:
                    # Reset empty space cells
                    cell.config(bg="white", text="", relief=tk.FLAT, bd=0, fg="white")
        
        # Force GUI update after clearing
        self.root.update_idletasks()
        
        # Create a dictionary to track which indices map to each position
        position_indices = {}
        for index, pos in self.index_to_position.items():
            if pos not in position_indices:
                position_indices[pos] = []
            position_indices[pos].append(index)
        
        # Map each character to its corresponding grid position
        for index, char in enumerate(pattern_string):
            if index in self.index_to_position:
                row, col = self.index_to_position[index]
                cell = self.cells[(row, col)]
                
                # Get all indices that map to this position
                indices_at_position = position_indices[(row, col)]
                
                # Create display text showing all indices
                if len(indices_at_position) == 1:
                    display_text = f"{char}\n({index})"
                else:
                    indices_str = ",".join(str(i) for i in sorted(indices_at_position))
                    display_text = f"{char}\n({indices_str})"
                
                # Set cell appearance based on character
                if char == 'W':
                    cell.config(bg="white", fg="black", text=display_text, 
                               relief=tk.RAISED, bd=2)
                elif char == 'B':
                    cell.config(bg="black", fg="white", text=display_text, 
                               relief=tk.RAISED, bd=2)
                elif char == 'x':
                    cell.config(bg="red", fg="white", text=display_text, 
                               relief=tk.RAISED, bd=2)

def create_multiple_windows(filenames):
    """Create multiple GUI windows for multiple files"""
    windows = []
    apps = []
    
    for i, filename in enumerate(filenames):
        # Create a new Tk window for each file
        root = tk.Toplevel() if i > 0 else tk.Tk()
        
        # Position windows side by side with better spacing
        x_offset = i * 820  # Offset each window by 820 pixels (800 + 20 margin)
        root.geometry(f"800x700+{x_offset}+50")
        
        # Create the app instance
        app = GridPatternGUI(root, filename)
        
        windows.append(root)
        apps.append(app)
    
    return windows, apps

def main():
    # Define the three filenames you want to open
    filenames = ["board1.txt", "board2.txt"]
    
    # Create multiple windows
    windows, apps = create_multiple_windows(filenames)
    
    # Start the main event loop
    if windows:
        windows[0].mainloop()

if __name__ == "__main__":
    main()