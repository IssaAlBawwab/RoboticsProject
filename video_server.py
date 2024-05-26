import grpc
import cv2
import numpy as np
from concurrent import futures
import video_streaming_pb2
import video_streaming_pb2_grpc

class VideoStreamingServicer(video_streaming_pb2_grpc.VideoStreamingServiceServicer):
    def StreamVideo(self, request_iterator, context):
        for video_frame in request_iterator:
            frame = np.frombuffer(video_frame.frame, dtype=np.uint8)
            frame = cv2.imdecode(frame, cv2.IMREAD_COLOR)

            # Display the frame
            cv2.imshow('Received Video', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        
        cv2.destroyAllWindows()
        return video_streaming_pb2.VideoResponse(message="Stream ended")

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    video_streaming_pb2_grpc.add_VideoStreamingServiceServicer_to_server(VideoStreamingServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
