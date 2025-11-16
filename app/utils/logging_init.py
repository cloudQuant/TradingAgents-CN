"""
Windows console encoding initialization for emoji support
"""
import sys
import logging


def init_windows_encoding():
    """Initialize Windows console encoding for emoji/Unicode support"""
    if sys.platform == 'win32':
        try:
            import io
            # Reconfigure stdout and stderr to use UTF-8
            sys.stdout = io.TextIOWrapper(
                sys.stdout.buffer, 
                encoding='utf-8',
                errors='replace',  # Replace unencodable characters
                line_buffering=True
            )
            sys.stderr = io.TextIOWrapper(
                sys.stderr.buffer, 
                encoding='utf-8',
                errors='replace',
                line_buffering=True
            )
            print("[INFO] Windows console encoding set to UTF-8")
            return True
        except Exception as e:
            print(f"[WARN] Failed to set UTF-8 encoding: {e}")
            return False
    return True


def configure_logging_encoding():
    """Configure logging to handle Unicode properly"""
    try:
        # Get root logger
        root_logger = logging.getLogger()
        
        # Update all handlers to use UTF-8
        for handler in root_logger.handlers:
            if hasattr(handler, 'stream'):
                try:
                    import io
                    if sys.platform == 'win32':
                        handler.stream = io.TextIOWrapper(
                            handler.stream.buffer,
                            encoding='utf-8',
                            errors='replace'
                        )
                except Exception:
                    pass
        
        return True
    except Exception as e:
        print(f"[WARN] Failed to configure logging encoding: {e}")
        return False


# Auto-initialize on import
init_windows_encoding()
