from fastapi import status
from fastapi.responses import JSONResponse
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.modules.auth.student.models import Student
from src.modules.profile.student.interface import Update_Student

from src.utils.validations import check_phone



async def get_student_detail(email : str, db:AsyncSession):

    try:
        result = await db.execute(select(Student).where(Student.email == email))
        student = result.scalar_one_or_none()


        if not student:
            return JSONResponse(
                status_code = status.HTTP_404_NOT_FOUND,
                content = {
                    "sucess" : False,
                    "msg" : "Student with this email not found"
                }
            )

        print(student)

        '''

        l1 = []

        for s in student:
            l1.append({
                "name" : f"{s.first_name}  {s.last_name}",
                "age" : s.age, 
                "ph_no" : s.ph_no, 
                "email" : s.email
                })

        '''

        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "success": True,
                "msg" : "Data featch successfully",
                "student" : {
                    "id" : student.id,
                    "name" : f"{student.first_name}  {student.last_name}",
                    "age" : student.age, 
                    "ph_no" : student.ph_no, 
                    "email" : student.email
                }

            }

        )

    
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "success": False,
                "message": "Invalid Credential",
                "error" : str(e)
            },
        )




async def update_student_datails(data: Update_Student, db: AsyncSession):

    try: 
        student_fetch_query = await db.execute(
            select(Student).where(Student.id == data.id)
        )

        student = student_fetch_query.scalar_one_or_none()
        if not student:
            return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content={
                    "success" : False,
                    "msg" : "Student with this id doesn't exists"
                }
            )


        student.first_name = data.first_name
        student.last_name = data.last_name
        student.age = data.age
        student.ph_no = check_phone(data.ph_no)

        await db.commit()

        await db.refresh(student)

        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content = {
                "success" : True,
                "msg" : "Details updated successfully"
            }
        )

    except:
        import traceback
        traceback.print_exc()
        raise






