import cv2
import grpc
import video_streaming_pb2
import video_streaming_pb2_grpc

def generate_video_frames():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Could not open webcam.")
        return

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        _, buffer = cv2.imencode('.jpg', frame)
        frame_bytes = buffer.tobytes()

        yield video_streaming_pb2.VideoFrame(frame=frame_bytes)

    cap.release()

def run():
    channel = grpc.insecure_channel('add_ip:50051')
    stub = video_streaming_pb2_grpc.VideoStreamingServiceStub(channel)

    response = stub.StreamVideo(generate_video_frames())
    print(response.message)

if __name__ == '__main__':
    run()
