from typing import List
from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status, Response
from sqlalchemy import func
import schemas.employee as schemas
from config.db import get_db
import models.employee as models
from sqlalchemy.orm import Session
from oauth2 import get_current_admin
from fastapi.staticfiles import StaticFiles
from typing import List
from facedetection import detect_faces_in_dataset,train_classifier

router = APIRouter(
    prefix='/employee',
    tags=['Employees']
)

# Show all employees
@router.get('/', response_model=List[schemas.AllEmployee], status_code=status.HTTP_200_OK)
def show_all(
        db: Session = Depends(get_db),
        current_admin: schemas.Admin = Depends(get_current_admin)
):
    employees = db.query(models.Employee).all()
    return employees


# Create Employee
@router.post('/', status_code=status.HTTP_201_CREATED)
def create(
        request: schemas.InEmployee,
        db: Session = Depends(get_db),
        current_admin: schemas.Admin = Depends(get_current_admin)
):
    new_employee = models.Employee(
        name=request.name,
        NIK=request.NIK,
        gender=request.gender,
        job_id=request.job_id,
        general_status_id=request.general_status_id
    )
    db.add(new_employee)
    db.commit()
    db.refresh(new_employee)
    return new_employee


# Show Employee by ID
@router.get('/{id}', status_code=status.HTTP_200_OK)
def show(
        id,
        db: Session = Depends(get_db),
        current_admin: schemas.Admin = Depends(get_current_admin)
):
    show_employee = db.query(models.Employee).filter(
        models.Employee.id == id).first()
    if not show_employee:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Employee with the ID {id} is not available")
    return show_employee


# Show Employee by name
@router.get('/search_by_name', status_code=status.HTTP_200_OK)
def show_name(
        name,
        db: Session = Depends(get_db),
        current_admin: schemas.Admin = Depends(get_current_admin)
):
    show_employee = db.query(models.Employee).filter(
        models.Employee.name.like(f"%{name}%")).all()
    return show_employee


# Update Employee
@router.put('/{id}', status_code=status.HTTP_202_ACCEPTED)
def update(
        id,
        request: schemas.UpdateEmployee,
        db: Session = Depends(get_db),
        current_admin: schemas.Admin = Depends(get_current_admin)
):
    employee = db.query(models.Employee).filter(models.Employee.id == id)
    if not employee.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Employee with ID {id} not found')

    employee.update(request.dict())
    db.commit()
    return 'Updated'


# Delete Employee
@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete(
        id,
        db: Session = Depends(get_db),
        current_admin: schemas.Admin = Depends(get_current_admin)
):
    employee = db.query(models.Employee).filter(models.Employee.id == id)
    if not employee.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Employee with ID {id} not found')
    employee.delete(synchronize_session=False)
    db.commit()
    return 'Done'


# # Fungsi untuk menyimpan informasi gambar ke MySQL
# def save_image_info_to_mysql(image: Image):
#     connection = pymysql.connect(
#         host='localhost',
#         user='root',
#         password='password',
#         db='test_db',
#         charset='utf8mb4',
#         cursorclass=pymysql.cursors.DictCursor
#     )

#     try:
#         with connection.cursor() as cursor:
#             # Create a new record
#             sql = "INSERT INTO `image` (`id`, `filename`) VALUES (%s, %s)"
#             cursor.execute(sql, (image.id, image.filename))

#         # connection is not autocommit by default. So you must commit to save your changes.
#         connection.commit()

#     finally:
#         connection.close()


# Upload Image
# @router.post("/upload", status_code=status.HTTP_201_CREATED)
# async def upload_image(
#     response: Response,
#     photo: UploadFile = File(...),
#     db: Session = Depends(get_db),
#     current_admin: schemas.Admin = Depends(get_current_admin)
# ):
#     FILEPATH = "./static/images/"
#     filename = photo.filename
#     extension = filename.split(".")[1]
#     emplo_id = filename.split(".")[0]
#     allowed_extensions = ["png", "jpg", "jpeg"]

#     if extension not in allowed_extensions:
#         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
#                             detail="File extension not allowed. Please upload a PNG or JPEG image.")

#     lastid = db.query(func.ifnull(func.max(models.Dataset.id), 0)).scalar()
#     img_id = lastid+1
#     token_name = f"{emplo_id}.{img_id}.{extension}"
#     generated_name = FILEPATH + token_name
#     file_content = await photo.read()

#     with open(generated_name, "wb") as file:
#         file.write(file_content)

#     # Save image info to the database
#     new_image = models.Dataset(
#         employee_id=photo.filename, img_employe=token_name)
#     db.add(new_image)
#     db.commit()

#     response.headers["Content-Type"] = "application/json"
#     return {"detail": "Image uploaded successfully"}


# Upload Multiple Images
@router.post("/upload", status_code=status.HTTP_201_CREATED)
async def upload_images(
    response: Response,
    photos: List[UploadFile] = File(...),
    db: Session = Depends(get_db),
    current_admin: schemas.Admin = Depends(get_current_admin)
):
    FILEPATH = "../static/images/"
    allowed_extensions = ["png", "jpg", "jpeg"]
    uploaded_images = []

    for photo in photos:
        filename = photo.filename
        extension = filename.split(".")[1]
        emplo_id = filename.split(".")[0]

        if extension not in allowed_extensions:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="File extension not allowed. Please upload a PNG or JPEG image.")

        last_id = db.query(func.ifnull(
            func.max(models.Dataset.id), 0)).scalar()
        img_id = last_id + 1
        token_name = f"{emplo_id}.{img_id}.{extension}"
        generated_name = FILEPATH + token_name
        file_content = await photo.read()

        with open(generated_name, "wb") as file:
            file.write(file_content)

        new_image = models.Dataset(
            employee_id=photo.filename, img_employe=token_name)
        db.add(new_image)
        uploaded_images.append(token_name)

    db.commit()

    detect_faces_in_dataset()
    train_classifier()

    print(generated_name)

    response.headers["Content-Type"] = "application/json"
    return {"detail": "Images uploaded successfully", "uploaded_images": uploaded_images}
