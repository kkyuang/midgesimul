import cv2
import numpy as np

def draw_motion_vectors(frame, flow, step=16, color=(0, 255, 0)):
    h, w = frame.shape[:2]
    y, x = np.mgrid[step/2:h:step, step/2:w:step].reshape(2, -1).astype(int)
    fx, fy = flow[y, x].T
    lines = np.vstack([x, y, x+fx, y+fy]).T.reshape(-1, 2, 2)
    lines = np.int32(lines + 0.5)
    for (x1, y1), (x2, y2) in lines:
        cv2.line(frame, (x1, y1), (x2, y2), color, 1)
        cv2.circle(frame, (x2, y2), 1, color, -1)
    return frame

def extract_motion_vectors(video_path, output_path):
    cap = cv2.VideoCapture(video_path)
    ret, prev_frame = cap.read()
    prev_gray = cv2.cvtColor(prev_frame, cv2.COLOR_BGR2GRAY)
    h, w = prev_gray.shape[:2]
    
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter(output_path, fourcc, 20.0, (w, h))
    
    font = cv2.FONT_HERSHEY_SIMPLEX
    y_count_pos = (10, h - 10)
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Calculate optical flow (motion vectors)
        flow = cv2.calcOpticalFlowFarneback(prev_gray, gray, None, 0.5, 3, 15, 3, 5, 1.2, 0)
        
        # Count positive and negative y values in motion vectors
        y_values = flow[..., 1].flatten()
        positive_y_count = np.sum(y_values > 0)
        negative_y_count = np.sum(y_values < 0)
        
        # Draw motion vectors on the frame
        frame_with_motion_vectors = draw_motion_vectors(frame.copy(), flow)
        
        # Write the frame to the output video
        out.write(frame_with_motion_vectors)
        
        # Display positive and negative y counts
        cv2.putText(frame_with_motion_vectors, f'Positive Y: {positive_y_count}', y_count_pos, font, 0.5, (255, 255, 255), 1, cv2.LINE_AA)
        cv2.putText(frame_with_motion_vectors, f'Negative Y: {negative_y_count}', (y_count_pos[0], y_count_pos[1] - 20), font, 0.5, (255, 255, 255), 1, cv2.LINE_AA)
        
        prev_gray = gray
    
    cap.release()
    out.release()

# Example usage
video_path = 'video01.mp4'
output_path = 'output_video_with_motion_vectors.avi'
extract_motion_vectors(video_path, output_path)
