import React, {useState, useEffect} from "react" //use efect despues de renderizar se ejecuta
const API = process.env.REACT_APP_API
const API_USER = process.env.REACT_USER_API

export const Processes = () => {
    const [name, setName] = useState ("")
    const [status, setStatus] = useState ("")
    const [process, setProcess] = useState([])
    const[editing, setEdit]=useState(false)
    const[id, setId]=useState("")
    const handleSubmit = async (e) => {
        e.preventDefault(); //cancela el evento y no vuelve a refrescar
        //CON FETCH PUEDO HACER LA PETICION A LA API
        //USO STRINGIFY PARA PODER CASTEAR EL BODY A STR PARA QUE NO HAYA PROBLEMAS DE CONVERSION
       if (!editing){
        const res = await fetch(`${API}/process`, {
            method: "POST",
            headers:
            {
                "Content-Type": "application/json" //el header es para informar el tipo de dato que enviaremos
            },
            body: JSON.stringify({
                name: name,
                status: "created and not started" //acordar status

            })
        
        })
        const data = await res.json();
        console.log(data)
        }
        else{
            const res = await fetch(`${API}/process/${id}`, {
                method: "PUT",
                headers:
                {
                    "Content-Type": "application/json" //el header es para informar el tipo de dato que enviaremos
                },
                body: JSON.stringify({
                    name: name,
                    status: status
                })
            
            })
            const data = await res.json();
            console.log(data)
            window.alert("Process updated")
        }
 //coloco la direccion a donde va a estar mi backend ESTA EN EL .ENV
        await getProcesses();
        setName("")
        setStatus("")
    }
    const getProcesses = async () => {
        const res = await fetch(`${API}/processes`) 
        const data = await res.json();
        setProcess(data)
    }
    
    useEffect(() => {
        getProcesses();
    }, [])
    
    // const deleteUser = async (id) => {
    //    const userRes = window.confirm("Are you sure you want to delete this process?")
    //    if (userRes){ 
    //         const res = await fetch(`${API}/process/${id}/`,{
    //             method: "DELETE"
    //         })
    //         const data = await res.json();
    //         console.log(data)
    //         await getProcesses();
    //     }
    // }
    // const editProcess = async (id) => {
    //     const res = await fetch(`${API}/process/${id}/`)
    //     const data = await res.json();
    //     setEdit(true);
    //     setId(data._id);
    //     setName(data.name)
    //     setStatus(data.status)
    //     console.log(data)
    //     await getProcesses();
    // }

    return(<div className="row">
        <div className="col-md-10">
            <form onSubmit={handleSubmit} className="card card-body">
                <div className="form-group">
                    <input type="text" onChange={e => setName(e.target.value)} 
                    value={name}
                    className="form-control"
                    placeholder="Name"
                    autoFocus
                    />
                </div>
                {/* <div className="form-group">
                    <input type="text" onChange={e => setStatus(e.target.value)} 
                    value={status}
                    className="form-control"
                    placeholder="Status"
                    />
                </div> */}
                <button className="btn btn-primary btn-block">
                    Create Process
                </button>
            </form>
        </div>
        <div className="col-md-6 m-4">
                <table className="table table-striped">
                    <thead>
                        <tr>
                            <th>Name</th>
                            <th>Status</th>
                            <th>Time execution</th>
                            <th>Operations</th>
                        </tr>
                    </thead>
                    <tbody>
                           {process.map(process =>(
                               <tr key={process._id}>
                                   <td>${process.name}</td>
                                   <td>${process.status}</td>
                                   <td>${process.time_execution}</td>
                                   <td>
                                    {/* <button className="btn btn-secondary btn-sm btn-block"
                                    onClick={() => editProcess(process._id)}>
                                            Edit
                                    </button>
                                    <button 
                                    className="btn btn-danger btn-sm btn-block"
                                    onClick={() => deleteUser(process._id)}>
                                            Delete
                                    </button> */}
                                   </td>

                               </tr>
                            ))} 
                    </tbody>
                </table>
        </div>
    </div>)
}