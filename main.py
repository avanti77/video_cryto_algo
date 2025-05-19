import cv2
import os
import numpy as np
from encrypt_frame import encrypt_frame
from decrypt_frame import decrypt_frame
from generate_key import generate_key
from encrypt_metadata import encrypt_metadata
from decrypt_metadata import decrypt_metadata

def load_metadata(meta_path, encryption_key):
    with open(meta_path, "r") as f:
        encrypted_meta = f.read()
    return decrypt_metadata(encrypted_meta, encryption_key)

def decrypt_video(encrypted_video_path, output_video_path, metadata):
    cap = cv2.VideoCapture(encrypted_video_path)
    if not cap.isOpened():
        print(f"[ERROR] Could not open encrypted video: {encrypted_video_path}")
        return []

    fourcc = cv2.VideoWriter_fourcc(*'FFV1')  # Lossless codec
    out = None
    frame_index = 0
    decrypted_frames = []

    print("[INFO] Starting frame-by-frame decryption...")

    while True:
        ret, frame = cap.read()
        if not ret:
            print("[INFO] Finished reading all frames.")
            break

        key_hex = metadata.get(str(frame_index))
        if key_hex is None:
            print(f"[WARNING] No key found for frame {frame_index}. Skipping.")
            frame_index += 1
            continue

        key_bytes = bytes.fromhex(key_hex)
        decrypted = decrypt_frame(frame, key_bytes)
        decrypted_frames.append(decrypted)

        if out is None:
            h, w, _ = decrypted.shape
            out = cv2.VideoWriter(output_video_path, fourcc, 20.0, (w, h))
            print(f"[INFO] Output video initialized with resolution {w}x{h}")

        out.write(decrypted)
        frame_index += 1

    cap.release()
    if out:
        out.release()
        print("[INFO] Output video released.")
    print(f"[SUCCESS] Decryption complete. Saved as: {output_video_path}")
    return decrypted_frames

def compare_frames(original_frames, decrypted_frames):
    for idx, (f1, f2) in enumerate(zip(original_frames, decrypted_frames)):
        if not np.array_equal(f1, f2):
            print(f"[ERROR] Frame {idx} mismatch! Not pixel-perfect.")
            return False
    print("[SUCCESS] All frames match perfectly.")
    return True

def main(video_path, output_video_path, encryption_key):
    print("[INFO] Opening input video...")
    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        print(f"[ERROR] Could not open input video: {video_path}")
        return

    fourcc = cv2.VideoWriter_fourcc(*'FFV1')  # Lossless FFV1
    out = None
    metadata = {}
    frame_index = 0
    original_frames = []

    print("[INFO] Starting frame-by-frame encryption...")

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        original_frames.append(frame.copy())

        key_hex = generate_key(frame.tobytes())
        key_bytes = bytes.fromhex(key_hex)
        encrypted = encrypt_frame(frame, key_bytes)

        if out is None:
            h, w, _ = encrypted.shape
            out = cv2.VideoWriter(output_video_path, fourcc, 20.0, (w, h))
            print(f"[INFO] Output video initialized with resolution {w}x{h}")

        out.write(encrypted)
        metadata[str(frame_index)] = key_hex
        frame_index += 1

    cap.release()
    if out:
        out.release()
        print("[INFO] Encrypted video file released.")

    print(f"[INFO] Processed {frame_index} frames. Saving encrypted metadata...")
    encrypted_meta = encrypt_metadata(metadata, encryption_key)

    meta_path = output_video_path + ".meta"
    with open(meta_path, "w") as f:
        f.write(encrypted_meta)

    print("[SUCCESS] Encryption complete.")
    print(f"  - Encrypted video saved as: {output_video_path}")
    print(f"  - Metadata saved as: {meta_path}")

    print("[INFO] Starting decryption...")
    metadata = load_metadata(meta_path, encryption_key)
    decrypted_path = "decrypted_" + os.path.basename(video_path).replace('.mp4', '.avi')
    decrypted_frames = decrypt_video(output_video_path, decrypted_path, metadata)

    print("[INFO] Verifying pixel-perfect restoration...")
    compare_frames(original_frames, decrypted_frames)

if __name__ == "__main__":
    main("input_vid.mp4", "output_encrypted_video.avi", "my_secret_key")
