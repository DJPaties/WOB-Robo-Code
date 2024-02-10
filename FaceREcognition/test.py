# import face_recognition
# import os
# import numpy as np
# import math

# known_face_encodings = []
# known_face_names = []

# def face_confidence(face_distance, face_match_threshold=0.6):
#     range = (1.0 - face_match_threshold)
#     linear_val = (1.0- face_distance) / (range *2.0)
#     if face_distance > face_match_threshold:
#         return str(round(linear_val * 100, 2)) + ''
#     else:
#         value = (linear_val + ((1.0- linear_val) * math.pow((linear_val - 0.5) * 2, 0.2))) * 100
#         return str(round(value, 2)) + ''

# for image in os.listdir('Current'):
#     try:
#         face_image = face_recognition.load_image_file(f'Current/{image}')
#         face_encoding = face_recognition.face_encodings(face_image)[0]
#         known_face_encodings.append(face_encoding)
#         known_face_names.append(image)
#     except IndexError as e:
#         os.remove(os.path.join('Current',image))
# print(known_face_names)

# for imgs in os.listdir("Current"):
#     x=face_recognition.load_image_file(os.path.join("Current",imgs))
#     face_locations = face_recognition.face_locations(x)
#     face_encodings = face_recognition.face_encodings(x,face_locations)
#     # face_encodings = face_recognition.face_encodings(imgs, face_locations)
#     face_names = []
#     # print("HI again")
#     for face_encoding in face_encodings:
#         matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
#         name = 'Unknown'
#         confidence = ''
#         face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
#         best_match_index = np.argmin(face_distances)
#         if matches[best_match_index]:
#             name = known_face_names[best_match_index]
#             confidence = face_confidence(face_distances[best_match_index])
#         face_names.append(f'{name} {confidence}')    
        
#     print(face_names)


value = ["Uknown- "]

print((value[0].split(" "))[0])
print(value[0].replace("-","he"))