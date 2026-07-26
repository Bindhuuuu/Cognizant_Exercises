import React from "react";

function CourseDetails({ courses }) {

    return (

        <div>

            <h1>Course Details</h1>

            {
                courses.map((course) => (

                    <div key={course.id}>

                        <h2>{course.name}</h2>

                        <h4>{course.date}</h4>

                    </div>

                ))
            }

        </div>

    );

}

export default CourseDetails;