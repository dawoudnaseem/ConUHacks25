import cv2
import numpy as np
import urllib.request
import time

def get_color_name(hsv):
    """
    Convert HSV values to color names
    Returns the name of the closest matching color
    """
    # Extract Hue value
    h = hsv[0]
    s = hsv[1]
    v = hsv[2]
    
    # Define color ranges in HSV
    color_ranges = {
        'Red': ((0, 50, 50), (10, 255, 255)),
        'Orange': ((11, 50, 50), (20, 255, 255)),
        'Yellow': ((21, 50, 50), (35, 255, 255)),
        'Green': ((36, 50, 50), (85, 255, 255)),
        'Blue': ((86, 50, 50), (130, 255, 255)),
        'Purple': ((131, 50, 50), (155, 255, 255)),
        'Pink': ((156, 50, 50), (180, 255, 255))
    }
    
    # Check if values are too low (black) or too high (white)
    if v < 50:
        return "Black"
    if s < 50 and v > 200:
        return "White"
    if s < 50:
        return "Gray"
        
    # Find matching color range
    for color_name, (lower, upper) in color_ranges.items():
        if lower[0] <= h <= upper[0]:
            return color_name
            
    return "Unknown"

def main():
    # ESP32 camera URL - replace with your ESP32's IP address
    url = 'http://your_esp32_ip_address/cam-stream'
    
    # Size of the center rectangle for color detection
    rect_size = 50
    
    try:
        while True:
            # Get image from ESP32
            img_resp = urllib.request.urlopen(url)
            imgnp = np.array(bytearray(img_resp.read()), dtype=np.uint8)
            frame = cv2.imdecode(imgnp, -1)
            
            # Get frame dimensions
            height, width = frame.shape[:2]
            
            # Define center rectangle coordinates
            x = width//2 - rect_size//2
            y = height//2 - rect_size//2
            
            # Draw rectangle in center
            cv2.rectangle(frame, (x, y), (x + rect_size, y + rect_size), (0, 255, 0), 2)
            
            # Get center region
            center_region = frame[y:y+rect_size, x:x+rect_size]
            
            # Convert to HSV
            hsv = cv2.cvtColor(center_region, cv2.COLOR_BGR2HSV)
            
            # Get average HSV values in the region
            avg_hsv = np.mean(hsv, axis=(0,1)).astype(np.uint8)
            
            # Get color name
            color_name = get_color_name(avg_hsv)
            
            # Display color name
            cv2.putText(frame, f"Color: {color_name}", (10, 30), 
                       cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            
            # Show frame
            cv2.imshow('Color Recognition', frame)
            
            # Exit if 'q' is pressed
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
                
            time.sleep(0.1)  # Small delay to prevent overwhelming the ESP32
            
    except Exception as e:
        print(f"Error: {e}")
    finally:
        cv2.destroyAllWindows()

if __name__ == "__main__":
    main()