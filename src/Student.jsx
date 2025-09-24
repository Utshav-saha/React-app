

function Student(props){

    return(
        <div className="text-lg border-4 p-8 border-red-500">
            <p>Name: {props.name}</p>
            <p>Age: {props.age}</p>
            <p>Student: {props.isStudent ? "Yes" : "No"}</p>
        </div>
    );

}

export default Student