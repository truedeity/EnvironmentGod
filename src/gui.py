import tkinter as tk
from tkinter import ttk, messagebox, filedialog, simpledialog
import os
from typing import Dict, Optional
from .env_manager import EnvironmentManager


class EnvironmentGUI:
    """Tkinter GUI for EnvironmentGod"""
    
    def __init__(self):
        self.env_manager = EnvironmentManager()
        self.root = tk.Tk()
        self.root.title("EnvironmentGod - Environment Variable Manager")
        self.root.geometry("900x700")
        self.root.minsize(800, 600)
        
        # Configure styles
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        self.setup_ui()
        self.refresh_variables()
    
    def setup_ui(self):
        """Set up the user interface"""
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)  
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(2, weight=1)
        
        # Title
        title_label = ttk.Label(main_frame, text="EnvironmentGod", 
                               font=('Arial', 16, 'bold'))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 10))
        
        # Control frame
        control_frame = ttk.LabelFrame(main_frame, text="Controls", padding="10")
        control_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), 
                          pady=(0, 10))
        control_frame.columnconfigure(1, weight=1)
        
        # Variable name entry
        ttk.Label(control_frame, text="Name:").grid(row=0, column=0, sticky=tk.W, padx=(0, 5))
        self.name_entry = ttk.Entry(control_frame, width=30)
        self.name_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(0, 10))
        
        # Variable value entry  
        ttk.Label(control_frame, text="Value:").grid(row=1, column=0, sticky=tk.W, padx=(0, 5))
        self.value_entry = ttk.Entry(control_frame, width=30)
        self.value_entry.grid(row=1, column=1, sticky=(tk.W, tk.E), padx=(0, 10))
        
        # Persistent checkbox
        self.persistent_var = tk.BooleanVar()
        persistent_cb = ttk.Checkbutton(control_frame, text="Persistent", 
                                       variable=self.persistent_var)
        persistent_cb.grid(row=2, column=1, sticky=tk.W, pady=(5, 0))
        
        # Buttons frame
        buttons_frame = ttk.Frame(control_frame)
        buttons_frame.grid(row=0, column=2, rowspan=3, padx=(10, 0))
        
        ttk.Button(buttons_frame, text="Set", command=self.set_variable).pack(pady=2, fill=tk.X)
        ttk.Button(buttons_frame, text="Get", command=self.get_variable).pack(pady=2, fill=tk.X)
        ttk.Button(buttons_frame, text="Delete", command=self.delete_variable).pack(pady=2, fill=tk.X)
        ttk.Button(buttons_frame, text="Clear", command=self.clear_entries).pack(pady=2, fill=tk.X)
        
        # Search frame
        search_frame = ttk.Frame(main_frame)
        search_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S))
        search_frame.columnconfigure(0, weight=1)
        search_frame.rowconfigure(1, weight=1)
        
        # Search controls
        search_controls = ttk.Frame(search_frame)
        search_controls.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        search_controls.columnconfigure(1, weight=1)
        
        ttk.Label(search_controls, text="Search:").grid(row=0, column=0, padx=(0, 5))
        self.search_entry = ttk.Entry(search_controls)
        self.search_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(0, 10))
        self.search_entry.bind('<KeyRelease>', self.on_search)
        
        # Filter options
        filter_frame = ttk.Frame(search_controls)
        filter_frame.grid(row=0, column=2, padx=(10, 0))
        
        self.show_all_var = tk.BooleanVar(value=True)
        ttk.Radiobutton(filter_frame, text="All", variable=self.show_all_var, 
                       value=True, command=self.refresh_variables).pack(side=tk.LEFT)
        ttk.Radiobutton(filter_frame, text="Saved", variable=self.show_all_var, 
                       value=False, command=self.refresh_variables).pack(side=tk.LEFT)
        
        ttk.Button(search_controls, text="Refresh", 
                  command=self.refresh_variables).grid(row=0, column=3, padx=(10, 0))
        
        # Treeview for variables
        tree_frame = ttk.Frame(search_frame)
        tree_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        tree_frame.columnconfigure(0, weight=1)
        tree_frame.rowconfigure(0, weight=1)
        
        # Create treeview with scrollbars
        self.tree = ttk.Treeview(tree_frame, columns=('Value', 'Persistent', 'Safety'), 
                                show='tree headings', height=15)
        self.tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure columns
        self.tree.heading('#0', text='Variable Name')
        self.tree.heading('Value', text='Value')
        self.tree.heading('Persistent', text='Persistent')
        self.tree.heading('Safety', text='Safety')
        
        self.tree.column('#0', width=200)
        self.tree.column('Value', width=350)
        self.tree.column('Persistent', width=80)
        self.tree.column('Safety', width=100)
        
        # Scrollbars
        v_scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.tree.yview)
        v_scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        self.tree.configure(yscrollcommand=v_scrollbar.set)
        
        h_scrollbar = ttk.Scrollbar(tree_frame, orient=tk.HORIZONTAL, command=self.tree.xview)
        h_scrollbar.grid(row=1, column=0, sticky=(tk.W, tk.E))
        self.tree.configure(xscrollcommand=h_scrollbar.set)
        
        # Bind tree selection
        self.tree.bind('<<TreeviewSelect>>', self.on_tree_select)
        self.tree.bind('<Double-1>', self.on_tree_double_click)
        
        # Menu bar
        self.create_menu()
        
        # Status bar
        self.status_var = tk.StringVar()
        status_bar = ttk.Label(main_frame, textvariable=self.status_var, 
                              relief=tk.SUNKEN, anchor=tk.W)
        status_bar.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(10, 0))
        
        self.update_status("Ready")
    
    def create_menu(self):
        """Create application menu"""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Import...", command=self.import_variables)
        file_menu.add_command(label="Export All...", command=self.export_all_variables)
        file_menu.add_command(label="Export Selected...", command=self.export_selected_variables)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)
        
        # Edit menu
        edit_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Edit", menu=edit_menu)
        edit_menu.add_command(label="Clear All Entries", command=self.clear_entries)
        edit_menu.add_command(label="Copy Name", command=self.copy_selected_name)
        edit_menu.add_command(label="Copy Value", command=self.copy_selected_value)
        
        # View menu
        view_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="View", menu=view_menu)
        view_menu.add_command(label="Refresh", command=self.refresh_variables)
        view_menu.add_command(label="Show All Variables", 
                             command=lambda: self.set_filter(True))
        view_menu.add_command(label="Show Saved Variables Only", 
                             command=lambda: self.set_filter(False))
    
    def set_filter(self, show_all: bool):
        """Set variable filter"""
        self.show_all_var.set(show_all)
        self.refresh_variables()
    
    def update_status(self, message: str):
        """Update status bar"""
        self.status_var.set(message)
        self.root.update_idletasks()
    
    def clear_entries(self):
        """Clear input entries"""
        self.name_entry.delete(0, tk.END)
        self.value_entry.delete(0, tk.END)
        self.persistent_var.set(False)
    
    def set_variable(self):
        """Set environment variable"""
        name = self.name_entry.get().strip()
        value = self.value_entry.get()
        persistent = self.persistent_var.get()
        
        if not name:
            messagebox.showerror("Error", "Variable name cannot be empty")
            return
        
        success = self.env_manager.set_env_var(name, value, persistent)
        if success:
            status = "persistent" if persistent else "temporary"
            self.update_status(f"Set {status} variable: {name}")
            self.refresh_variables()
            messagebox.showinfo("Success", f"Variable '{name}' set successfully")
        else:
            messagebox.showerror("Error", f"Failed to set variable '{name}'")
    
    def get_variable(self):
        """Get environment variable"""
        name = self.name_entry.get().strip()
        if not name:
            messagebox.showerror("Error", "Variable name cannot be empty")
            return
        
        value = self.env_manager.get_env_var(name)
        if value is not None:
            self.value_entry.delete(0, tk.END)
            self.value_entry.insert(0, value)
            self.update_status(f"Retrieved variable: {name}")
        else:
            messagebox.showwarning("Not Found", f"Variable '{name}' not found")
    
    def delete_variable(self):
        """Delete environment variable with safety checks"""
        name = self.name_entry.get().strip()
        if not name:
            messagebox.showerror("Error", "Variable name cannot be empty")
            return
        
        persistent = self.persistent_var.get()
        
        # Check safety
        safety_info = self.env_manager.get_variable_safety_info(name)
        
        # Build confirmation message
        msg = f"Delete variable '{name}'"
        if persistent:
            msg += " (persistent)"
        msg += "?"
        
        # Add safety warnings
        if safety_info['is_protected']:
            msg = f"⚠️ PROTECTED VARIABLE ⚠️\n\n{safety_info['recommendation']}\n\n" + msg
            msg += "\n\nThis could seriously damage your system!"
        elif safety_info['is_sensitive']:
            msg = f"⚠️ SENSITIVE VARIABLE ⚠️\n\n{safety_info['recommendation']}\n\n" + msg
            msg += "\n\nThis could affect system functionality!"
        
        # Enhanced confirmation for protected variables
        if safety_info['is_protected']:
            # Double confirmation for protected variables
            if not messagebox.askyesno("⚠️ DANGER - Protected Variable", msg):
                return
            
            # Second confirmation
            second_msg = f"Are you ABSOLUTELY SURE you want to delete '{name}'?\n\n"
            second_msg += "This is a critical system variable and deletion may cause system instability!"
            if not messagebox.askyesno("⚠️ FINAL WARNING", second_msg):
                return
        elif safety_info['is_sensitive']:
            # Single strong confirmation for sensitive variables
            if not messagebox.askyesno("⚠️ Warning - Sensitive Variable", msg):
                return
        else:
            # Normal confirmation for user variables
            if not messagebox.askyesno("Confirm Delete", msg):
                return
        
        # Proceed with deletion
        force = safety_info['is_protected'] or safety_info['is_sensitive']
        success, message = self.env_manager.delete_env_var(name, persistent, force)
        
        if success:
            status = "persistent" if persistent else "temporary"
            self.update_status(f"Deleted {status} variable: {name}")
            self.refresh_variables()
            self.clear_entries()
            
            # Show success with warning if forced
            success_msg = f"Variable '{name}' deleted successfully"
            if force:
                success_msg += "\n\n⚠️ Warning: System variable was deleted!"
            messagebox.showinfo("Success", success_msg)
        else:
            messagebox.showerror("Error", message)
    
    def refresh_variables(self):
        """Refresh the variables tree"""
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Get variables based on filter
        if self.show_all_var.get():
            env_vars = self.env_manager.get_all_env_vars()
            saved_vars = self.env_manager.get_saved_vars()
        else:
            env_vars = self.env_manager.get_saved_vars()
            saved_vars = env_vars
        
        # Apply search filter
        search_term = self.search_entry.get().lower()
        
        count = 0
        for name, value in sorted(env_vars.items()):
            if (not search_term or 
                search_term in name.lower() or 
                search_term in value.lower()):
                
                is_persistent = "Yes" if name in saved_vars else "No"
                
                # Get safety information
                safety_info = self.env_manager.get_variable_safety_info(name)
                if safety_info['is_protected']:
                    safety_status = "🔒 Protected"
                elif safety_info['is_sensitive']:
                    safety_status = "⚠️ Sensitive"
                else:
                    safety_status = "✓ Safe"
                
                self.tree.insert('', 'end', text=name, 
                               values=(value, is_persistent, safety_status))
                count += 1
        
        self.update_status(f"Showing {count} variables")
    
    def on_search(self, event):
        """Handle search entry changes"""
        self.refresh_variables()
    
    def on_tree_select(self, event):
        """Handle tree selection"""
        selection = self.tree.selection()
        if selection:
            item = selection[0]
            name = self.tree.item(item, 'text')
            value = self.tree.item(item, 'values')[0]
            is_persistent = self.tree.item(item, 'values')[1] == "Yes"
            
            # Populate entries
            self.name_entry.delete(0, tk.END)
            self.name_entry.insert(0, name)
            self.value_entry.delete(0, tk.END)
            self.value_entry.insert(0, value)
            self.persistent_var.set(is_persistent)
    
    def on_tree_double_click(self, event):
        """Handle tree double-click"""
        self.get_variable()
    
    def copy_selected_name(self):
        """Copy selected variable name to clipboard"""
        selection = self.tree.selection()
        if selection:
            name = self.tree.item(selection[0], 'text')
            self.root.clipboard_clear()
            self.root.clipboard_append(name)
            self.update_status(f"Copied name: {name}")
    
    def copy_selected_value(self):
        """Copy selected variable value to clipboard"""
        selection = self.tree.selection()
        if selection:
            value = self.tree.item(selection[0], 'values')[0]
            self.root.clipboard_clear()
            self.root.clipboard_append(value)
            self.update_status(f"Copied value to clipboard")
    
    def import_variables(self):
        """Import variables from file"""
        filename = filedialog.askopenfilename(
            title="Import Variables",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        
        if filename:
            persistent = messagebox.askyesno("Import Options", 
                                           "Make imported variables persistent?")
            
            success = self.env_manager.import_env_vars(filename, persistent)
            if success:
                self.refresh_variables()
                status = "persistent" if persistent else "temporary"
                self.update_status(f"Imported {status} variables from {filename}")
                messagebox.showinfo("Success", "Variables imported successfully")
            else:
                messagebox.showerror("Error", "Failed to import variables")
    
    def export_all_variables(self):
        """Export all variables to file"""
        filename = filedialog.asksaveasfilename(
            title="Export All Variables",
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        
        if filename:
            success = self.env_manager.export_env_vars(filename)
            if success:
                self.update_status(f"Exported all variables to {filename}")
                messagebox.showinfo("Success", "Variables exported successfully")
            else:
                messagebox.showerror("Error", "Failed to export variables")
    
    def export_selected_variables(self):
        """Export selected variables to file"""
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select variables to export")
            return
        
        filename = filedialog.asksaveasfilename(
            title="Export Selected Variables",
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        
        if filename:
            var_names = [self.tree.item(item, 'text') for item in selection]
            success = self.env_manager.export_env_vars(filename, var_names)
            if success:
                self.update_status(f"Exported {len(var_names)} variables to {filename}")
                messagebox.showinfo("Success", "Selected variables exported successfully")
            else:
                messagebox.showerror("Error", "Failed to export variables")
    
    def run(self):
        """Run the GUI application"""
        self.root.mainloop()


def main():
    """Main GUI entry point"""
    app = EnvironmentGUI()
    app.run()


if __name__ == "__main__":
    main()
