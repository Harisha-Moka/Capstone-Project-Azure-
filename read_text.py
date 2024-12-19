import os
import time
from dotenv import load_dotenv
from PIL import Image, ImageDraw
from matplotlib import pyplot as plt
from azure.ai.vision import ImageAnalysisClient
from azure.ai.vision import ImageAnalysisResult
from azure.ai.vision.models import VisualFeatures
from azure.core.credentials import AzureKeyCredential


def main():
    global cv_client
    try:
        # Load environment variables
        load_dotenv()
        ai_endpoint = os.getenv('AI_SERVICE_ENDPOINT')
        ai_key = os.getenv('AI_SERVICE_KEY')

        if not ai_endpoint or not ai_key:
            raise ValueError("AI_SERVICE_ENDPOINT or AI_SERVICE_KEY not set in the .env file.")

        # Authenticate Azure AI Vision client
        cv_client = ImageAnalysisClient(
            endpoint=ai_endpoint,
            credential=AzureKeyCredential(ai_key)
        )

        # Menu for text reading functions
        print('\n1: Use Read API for image (Lincoln.jpg)\n2: Read handwriting (Note.jpg)\n'
              '3: Read Education image\n4: Read Transportation image\n5: Read Black-text image\nAny other key to quit\n')

        command = input('Enter a number: ')
        if command == '1':
            image_file = os.path.join('images', 'Lincoln.jpg')
            get_text_read(image_file)
        elif command == '2':
            image_file = os.path.join('images', 'Note.jpg')
            get_text_read(image_file)
        elif command == '3':
            image_file = os.path.join('images', 'Education.jpg')
            get_text_read(image_file)
        elif command == '4':
            image_file = os.path.join('images', 'transportation.jpg')
            get_text_read(image_file)
        elif command == '5':
            image_file = os.path.join('images', 'black-text.jpg')
            get_text_read(image_file)
        else:
            print("Exiting program.")
            return

    except Exception as ex:
        print(f"Error: {ex}")


def get_text_read(image_file):
    print('\n')

    try:
        # Open image file
        with open(image_file, "rb") as f:
            image_data = f.read()

        # Use Analyze image function to read text in image
        result = cv_client.analyze_image(
            image_data=image_data,
            visual_features=[VisualFeatures.read]
        )

        if result.read is not None:
            print("\nText detected:")
            # Prepare image for drawing
            image = Image.open(image_file)
            fig = plt.figure(figsize=(image.width / 100, image.height / 100))
            plt.axis('off')
            draw = ImageDraw.Draw(image)
            color = 'cyan'

            for block in result.read.blocks:
                for line in block.lines:
                    print(f"Text: {line.text}")
                    print(f"Bounding Polygon: {[(p.x, p.y) for p in line.bounding_polygon]}")

                    for word in line.words:
                        print(f"  Word: '{word.text}', Bounding Polygon: {[(p.x, p.y) for p in word.bounding_polygon]}, Confidence: {word.confidence:.4f}")

                        # Draw bounding box around word
                        bounding_polygon = [(p.x, p.y) for p in word.bounding_polygon]
                        draw.polygon(bounding_polygon, outline=color, width=3)

            # Save and display image with bounding polygons
            plt.imshow(image)
            plt.tight_layout(pad=0)
            outputfile = 'text_detected_output.jpg'
            fig.savefig(outputfile)
            print(f'\nResults saved in {outputfile}')
        else:
            print("No text detected in the image.")

    except Exception as e:
        print(f"Error reading image: {e}")


if __name__ == "__main__":
    main()
