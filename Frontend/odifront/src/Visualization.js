import React,{useState,useEffect} from "react";
import './Visualization.css'
function Visualization() {
    const [x,y] = useState('Hello');
    useEffect(() => {
        fetch('/test').then(res => res.json()).then(data=>{y(data.Name)});
        // console.log(fetch('/test').then(res => res.json()).then())
      }, []);

    return (
    <div className="vis">
        {x}
    </div>);
}

export default Visualization;