from pdf2image import convert_from_path
from os import listdir, makedirs
from models import Pitch, PitchImg
from app import SessionLocal


with SessionLocal() as db:
  for pdf_path in listdir("presentations"):
    print(f"Начал обработку {pdf_path}")
    pitchname = pdf_path[:pdf_path.rfind(".")]
    makedirs(f"static/pitches/{pitchname}")

    images = convert_from_path("presentations/" + pdf_path)
    pitch = Pitch(name=pitchname, avatar_name=f"../static/pitches/{pitchname}/page_1.png")
    db.add(pitch)
    db.commit()

    for i, image in enumerate(images):
        p = f"static/pitches/{pitchname}/page_{i+1}.png"
        image.save(p, "PNG")
        pitch_img = PitchImg(url="../" + p, pitch_id=pitch.id)
        db.add(pitch_img)
    db.commit()

    print(f"Конвертировал {pdf_path}")