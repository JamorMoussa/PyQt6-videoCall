import paho.mqtt.client as mqtt
import base64
import io
import cv2
from threading import Thread
import numpy as np

broker_address = "broker.hivemq.com"
broker_port = 1883
topic = "example_topic"

# Queue to store received images
image_queue = []

def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe(topic)

def on_message(client, userdata, msg):
    image = base64.b64decode(msg.payload.decode("utf-8"))

    # Read the image directly from memory without saving it
    image_np = cv2.imdecode(np.frombuffer(image, np.uint8), cv2.IMREAD_COLOR)

    # Resize the image to a smaller resolution (e.g., 640x480)
    image_np = cv2.resize(image_np, (640, 480))

    # Put the resized image in the queue for display
    image_queue.append(image_np.copy())

def display_image():
    while True:
        try:
            if image_queue:
                image_np = image_queue.pop(0)

                # Display the resized image using OpenCV
                cv2.imshow("Received Image", image_np)
                cv2.waitKey(100)  # Increase the delay to 100 milliseconds

        except Exception as e:
            print(f"An error occurred: {e}")

def main():
    subscriber = mqtt.Client("Subscriber")
    subscriber.on_connect = on_connect
    subscriber.on_message = on_message

    subscriber.connect(broker_address, broker_port)
    subscriber.loop_start()

    # Start the display_image function in a separate thread
    display_thread = Thread(target=display_image)
    display_thread.start()

    try:
        while True:
            pass
    except KeyboardInterrupt:
        print("Subscriber script terminated by user.")
    finally:
        subscriber.disconnect()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
