from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field


class CourseItem(BaseModel):
    courseId: str
    category: Optional[str] = None
    courseName: str
    courseDescription: Optional[str] = None
    whatYouWillLearn: Optional[str] = None


class RecommendationRequest(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    enrolled_courses: List[CourseItem] = Field(alias="enrolledCourses")
    all_courses: List[CourseItem] = Field(alias="allCourses")
