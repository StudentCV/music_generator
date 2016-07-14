import subprocess
import cv2
import pypylon.pylon as pylon

camera = pylon.InstantCamera(pylon.TlFactory.GetInstance().CreateFirstDevice())
camera.Open()
camera.PixelFormat = "RGB8"

while True:
    # Grab image, convert it to greyscale and run edge detection
    grab_result = camera.GrabOne(400)
    image = grab_result.Array
    image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    image_edge_detected = cv2.Canny(image_gray, 20, 250)

    # Detect contours and choose biggest one
    _source_image, contours, _hierarchy = \
        cv2.findContours(image_edge_detected.copy(), cv2.RETR_TREE,
                         cv2.CHAIN_APPROX_SIMPLE)
    if len(contours) == 0:
        print("No contours found!")
        continue
    contour = sorted(contours, key=cv2.contourArea, reverse=True)[:1][0]

    # Draw contours on original image
    cv2.drawContours(image, contours, -1, (0, 255, 0))
    cv2.imshow('image', image)

    # Extract drawing area
    x, y, w, h = cv2.boundingRect(contour)
    extract = image_gray.copy()[y:y+h, x:x+w]
    _ret1, extract_grey = cv2.threshold(extract, 100, 255, cv2.THRESH_BINARY)

    code = cv2.resize(extract_grey, (8, 7), interpolation=cv2.INTER_AREA)
    _ret2, code = cv2.threshold(code, 160, 255, cv2.THRESH_BINARY)

    # List of lists to store the extracted values
    result = [[element == 0 for element in row] for row in code]

    # Show the resulting matrix
    height, width = code.shape[:2]
    code_large = cv2.resize(code, (100*width, 100*height),
                            interpolation=cv2.INTER_AREA)
    _ret3, code_large = cv2.threshold(code_large, 160, 255, cv2.THRESH_BINARY)
    cv2.imshow('codeLarge', code_large)
    cv2.waitKey(100)

    # Dictionary matching the rows of the table to note values
    note_mappings = ['A4', 'E5', 'Ds5', 'Fs5', 'G5', 'Gs4', 'C6']
    music = ''

    # Iterate over the table and generate the 'music'
    for index, row in enumerate(result):
        music += 'live_loop :{} do \n'.format(note_mappings[index])
        for col in row:
            if col is True:
                music += 'play :{} \n'.format(note_mappings[index])
            else:
                music += 'sleep 0.1 \n'
        music += 'sleep 1 \n end \n'

    # Write music into new file
    print (music)
    with open('music', 'w') as outfile:
        outfile.write(music)
    # Parse the music file to sonic pi via sonic pi CLI
    subprocess.Popen('cat music | sonic_pi', shell=True)

    should_continue = input("New picture? y/n ")
    subprocess.Popen('sonic_pi stop', shell=True)

    if should_continue == 'y':
        continue
    else:
        # Exit the program and stop sonic pi if no new image is captured
        break

# Send stop command to sonic pi if program is closed
subprocess.Popen('sonic_pi stop', shell=True)
cv2.destroyAllWindows()
