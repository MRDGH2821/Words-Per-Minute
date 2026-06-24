"""Example usage of the modernized Words Per Minute application.

This script demonstrates different ways to use the WPM package.
"""

from pathlib import Path
from WPM import WPMApp, AppConfig


def example_1_default_configuration():
    """Example 1: Use default configuration with user prompts."""
    print("=" * 60)
    print("Example 1: Default Configuration")
    print("=" * 60)
    
    app = WPMApp()
    app.initialize()  # Will prompt user for configuration
    app.run()


def example_2_custom_configuration():
    """Example 2: Use custom configuration without prompts."""
    print("=" * 60)
    print("Example 2: Custom Configuration")
    print("=" * 60)
    
    # Create custom configuration
    config = AppConfig(
        font_size=120,
        words_per_second=2.5,  # 150 WPM
        paragraph_file=Path("para.txt"),
        background_color="Navy",
        text_color="Yellow",
        font_family="Helvetica"
    )
    
    app = WPMApp(config=config)
    app.initialize()
    app.run()


def example_3_programmatic_setup():
    """Example 3: Programmatic setup with custom paragraph."""
    print("=" * 60)
    print("Example 3: Programmatic Setup")
    print("=" * 60)
    
    # Create a custom paragraph file
    custom_para = Path("custom_para.txt")
    custom_para.write_text(
        "This is a custom paragraph created programmatically. "
        "You can load any text content this way. "
        "The application will display each word in sequence.",
        encoding="utf-8"
    )
    
    # Configure with custom settings
    config = AppConfig(
        font_size=100,
        words_per_second=3.0,  # 180 WPM - faster!
        paragraph_file=custom_para,
        background_color="Black",
        text_color="Lime"
    )
    
    app = WPMApp(config=config)
    app.initialize()
    app.run()


def example_4_word_reader_only():
    """Example 4: Use WordReader independently."""
    print("=" * 60)
    print("Example 4: Word Reader Only")
    print("=" * 60)
    
    from WPM import WordReader
    
    # Create a test file
    test_file = Path("test_para.txt")
    test_file.write_text(
        "The quick brown fox jumps over the lazy dog.",
        encoding="utf-8"
    )
    
    # Use WordReader independently
    reader = WordReader(test_file)
    
    print(f"Total words: {reader.total_words}")
    print(f"Current word: {reader.get_current_word()}")
    print(f"Progress: {reader.get_progress()}")
    
    # Iterate through words
    print("\nWords:")
    for i in range(reader.total_words):
        print(f"  {i+1}. {reader.next_word()}")
    
    print(f"\nProgress percentage: {reader.get_progress_percentage():.1f}%")
    
    # Clean up
    test_file.unlink()


def example_5_speed_comparison():
    """Example 5: Test different reading speeds."""
    print("=" * 60)
    print("Example 5: Speed Comparison")
    print("=" * 60)
    
    speeds = [
        (1.0, "Slow - 60 WPM"),
        (2.0, "Normal - 120 WPM"),
        (3.0, "Fast - 180 WPM"),
        (5.0, "Very Fast - 300 WPM"),
    ]
    
    print("\nAvailable speeds:")
    for wps, description in speeds:
        print(f"  {description}")
    
    choice = input("\nSelect speed (1-4): ").strip()
    try:
        idx = int(choice) - 1
        if 0 <= idx < len(speeds):
            wps, desc = speeds[idx]
            print(f"\nStarting with {desc}...")
            
            config = AppConfig(
                font_size=100,
                words_per_second=wps,
                paragraph_file=Path("para.txt")
            )
            
            app = WPMApp(config=config)
            app.initialize()
            app.run()
        else:
            print("Invalid choice!")
    except ValueError:
        print("Invalid input!")


def main():
    """Main menu for examples."""
    print("\n" + "=" * 60)
    print("Words Per Minute - Example Usage")
    print("=" * 60)
    print("\nSelect an example to run:")
    print("  1. Default Configuration (with prompts)")
    print("  2. Custom Configuration (preset values)")
    print("  3. Programmatic Setup (create file programmatically)")
    print("  4. Word Reader Only (no GUI)")
    print("  5. Speed Comparison (test different speeds)")
    print("  0. Exit")
    print("=" * 60)
    
    choice = input("\nEnter your choice (0-5): ").strip()
    
    examples = {
        "1": example_1_default_configuration,
        "2": example_2_custom_configuration,
        "3": example_3_programmatic_setup,
        "4": example_4_word_reader_only,
        "5": example_5_speed_comparison,
    }
    
    if choice == "0":
        print("Goodbye!")
        return
    
    if choice in examples:
        try:
            examples[choice]()
        except KeyboardInterrupt:
            print("\n\nInterrupted by user.")
        except Exception as e:
            print(f"\nError: {e}")
    else:
        print("Invalid choice!")


if __name__ == "__main__":
    main()