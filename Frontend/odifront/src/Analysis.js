import './Analysis.css'
import React,{useEffect,useState} from 'react';

async function Submit(user_text, set_text,setLoading)
{
    if (user_text!=='')
        {
            const arr=[];
            setLoading(true);
            // const [x, y] = useState('Hello');
            // fetch('/test').then(res => res.json()).then(data=>{y(data.Name)});
            const body = {"input": user_text};
            
            const response = await fetch('/api/test', {
                            method: 'POST',
                            headers: {
                                'Content-Type': 'application/json'
                            },
                            body: JSON.stringify(body)
                            });
            const data  = await response.json();
            data['Output'].forEach((val) => {arr.push(<li>{val}</li>)})
            set_text(arr);
            setLoading(false);
            console.log(data['Output']);
        }
    else
        {set_text("Retry!")}

}

function Analysis() {
    const[text,set_text] = useState('');
    const[answer, setAnswer] = useState('');
    const[loading, setLoading] = useState(false);


    const handleSubmit = (e) => {
        e.preventDefault(); // Prevent default form submission behavior
        Submit(text, setAnswer,setLoading);
    }

    

    return (
        <div className='Container'>
            <div className='InnerContainer'>
                <h1>ODI Analysis</h1>
            </div>
            <div className="search-container">
                <form action=""  method="get" className="forms" onSubmit={handleSubmit}>
                    <input type="text" placeholder="Search..." name="search" value={text} onChange={(e)=>{set_text(e.target.value)}}/>
                    <button type="submit"  ><i class="fa fa-search"></i></button>
                </form>
                </div>
                <div className='InnerContainer'>
                {loading ? (
                    <div>Loading...</div> // Show loading message or video
                ) : (
                    <div className='output' >{answer}</div> // Show answer when not loading
                )}
            </div>
        </div>

    );
}

export default Analysis;