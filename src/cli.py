import argparse
import sys
import os
from typing import List
from .env_manager import EnvironmentManager


class EnvironmentCLI:
    """Command-line interface for EnvironmentGod"""
    
    def __init__(self):
        self.env_manager = EnvironmentManager()
        self.parser = self._create_parser()
    
    def _create_parser(self) -> argparse.ArgumentParser:
        """Create command-line argument parser"""
        parser = argparse.ArgumentParser(
            prog='EnvironmentGod',
            description='Manage environment variables from command line',
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog="""
Examples:
  envgod set MY_VAR "my_value"           # Set temporary variable
  envgod set MY_VAR "my_value" --persist # Set persistent variable  
  envgod get MY_VAR                      # Get variable value
  envgod delete MY_VAR --persist         # Delete persistent variable
  envgod list                            # List all variables
  envgod search "path"                   # Search variables
  envgod export vars.json                # Export all variables
  envgod import vars.json --persist      # Import variables
            """
        )
        
        subparsers = parser.add_subparsers(
            dest='command', 
            help='Available commands'
        )
        
        # Set command
        set_parser = subparsers.add_parser('set', help='Set environment variable')
        set_parser.add_argument('name', help='Variable name')
        set_parser.add_argument('value', help='Variable value')
        set_parser.add_argument('--persist', '-p', action='store_true', 
                               help='Make variable persistent')
        
        # Get command
        get_parser = subparsers.add_parser('get', help='Get environment variable')
        get_parser.add_argument('name', help='Variable name')
        
        # Delete command
        del_parser = subparsers.add_parser('delete', help='Delete environment variable')
        del_parser.add_argument('name', help='Variable name')
        del_parser.add_argument('--persist', '-p', action='store_true',
                               help='Delete persistent variable')
        del_parser.add_argument('--force', '-f', action='store_true',
                               help='Force deletion of protected/sensitive variables')
        
        # List command
        list_parser = subparsers.add_parser('list', help='List environment variables')
        list_parser.add_argument('--saved', '-s', action='store_true',
                                help='Show only saved persistent variables')
        
        # Search command
        search_parser = subparsers.add_parser('search', help='Search environment variables')
        search_parser.add_argument('term', help='Search term')
        
        # Export command
        export_parser = subparsers.add_parser('export', help='Export environment variables')
        export_parser.add_argument('filename', help='Output filename')
        export_parser.add_argument('--vars', nargs='+', help='Specific variables to export')
        
        # Import command
        import_parser = subparsers.add_parser('import', help='Import environment variables')
        import_parser.add_argument('filename', help='Input filename')
        import_parser.add_argument('--persist', '-p', action='store_true',
                                  help='Make imported variables persistent')
        import_parser.add_argument('--no-flatten', action='store_true',
                                  help='Disable automatic flattening of nested JSON')
        
        return parser
    
    def run(self, args: List[str] = None) -> int:
        """Run CLI with given arguments"""
        if args is None:
            args = sys.argv[1:]
        
        if not args:
            self.parser.print_help()
            return 0
        
        parsed_args = self.parser.parse_args(args)
        
        try:
            return self._execute_command(parsed_args)
        except Exception as e:
            print(f"Error: {e}")
            return 1
    
    def _execute_command(self, args) -> int:
        """Execute the parsed command"""
        if args.command == 'set':
            return self._cmd_set(args)
        elif args.command == 'get':
            return self._cmd_get(args)
        elif args.command == 'delete':
            return self._cmd_delete(args)
        elif args.command == 'list':
            return self._cmd_list(args)
        elif args.command == 'search':
            return self._cmd_search(args)
        elif args.command == 'export':
            return self._cmd_export(args)
        elif args.command == 'import':
            return self._cmd_import(args)
        else:
            self.parser.print_help()
            return 0
    
    def _cmd_set(self, args) -> int:
        """Handle set command"""
        success = self.env_manager.set_env_var(args.name, args.value, args.persist)
        if success:
            status = "persistent" if args.persist else "temporary"
            print(f"[OK] Set {status} variable: {args.name} = {args.value}")
            return 0
        else:
            print(f"[ERROR] Failed to set variable: {args.name}")
            return 1
    
    def _cmd_get(self, args) -> int:
        """Handle get command"""
        value = self.env_manager.get_env_var(args.name)
        if value is not None:
            print(f"{args.name} = {value}")
            return 0
        else:
            print(f"Variable not found: {args.name}")
            return 1
    
    def _cmd_delete(self, args) -> int:
        """Handle delete command"""
        # Check safety first
        safety_info = self.env_manager.get_variable_safety_info(args.name)
        
        if not args.force:
            if safety_info['is_protected']:
                print(f"[ERROR] {safety_info['recommendation']}")
                print(f"Use --force to override protection for '{args.name}'")
                return 1
            elif safety_info['is_sensitive']:
                print(f"[WARNING] {safety_info['recommendation']}")
                print(f"Use --force to confirm deletion of '{args.name}'")
                return 1
        
        success, message = self.env_manager.delete_env_var(args.name, args.persist, args.force)
        if success:
            status = "persistent" if args.persist else "temporary"
            print(f"[OK] Deleted {status} variable: {args.name}")
            if args.force:
                print("[WARNING] Used force override")
            return 0
        else:
            print(f"[ERROR] {message}")
            return 1
    
    def _cmd_list(self, args) -> int:
        """Handle list command"""
        if args.saved:
            vars_dict = self.env_manager.get_saved_vars()
            print("Saved persistent variables:")
        else:
            vars_dict = self.env_manager.get_all_env_vars()
            print("All environment variables:")
        
        if not vars_dict:
            print("No variables found.")
            return 0
        
        # Sort and display
        for name, value in sorted(vars_dict.items()):
            print(f"{name} = {value}")
        
        print(f"\nTotal: {len(vars_dict)} variables")
        return 0
    
    def _cmd_search(self, args) -> int:
        """Handle search command"""
        results = self.env_manager.search_env_vars(args.term)
        if results:
            print(f"Variables matching '{args.term}':")
            for name, value in sorted(results.items()):
                print(f"{name} = {value}")
            print(f"\nFound: {len(results)} variables")
        else:
            print(f"No variables found matching '{args.term}'")
        return 0
    
    def _cmd_export(self, args) -> int:
        """Handle export command"""
        success = self.env_manager.export_env_vars(args.filename, args.vars)
        if success:
            print(f"[OK] Exported variables to: {args.filename}")
            return 0
        else:
            print(f"[ERROR] Failed to export variables to: {args.filename}")
            return 1
    
    def _cmd_import(self, args) -> int:
        """Handle import command"""
        if not os.path.exists(args.filename):
            print(f"File not found: {args.filename}")
            return 1
        
        flatten = not args.no_flatten
        success = self.env_manager.import_env_vars(args.filename, args.persist, flatten)
        if success:
            status = "persistent" if args.persist else "temporary"  
            flatten_info = " (flattened)" if flatten else " (as-is)"
            print(f"[OK] Imported {status} variables from: {args.filename}{flatten_info}")
            return 0
        else:
            print(f"[ERROR] Failed to import variables from: {args.filename}")
            return 1


def main():
    """Main CLI entry point"""
    cli = EnvironmentCLI()
    return cli.run()


if __name__ == "__main__":
    sys.exit(main())
