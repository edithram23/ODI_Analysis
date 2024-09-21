import './Visualization.css'
import React,{useEffect,useState} from 'react';
import Output from './Output';
// import img_bg from './img/img1.jpg';
import img_bg from './assets/img/img1.jpg';
async function Submit(user_text,user_text2, set_text,setLoading)
{
    if (user_text!=='' & user_text2!=='')
        {
            const arr=[];
            setLoading(true);
            // const [x, y] = useState('Hello');
            // fetch('/test').then(res => res.json()).then(data=>{y(data.Name)});
            const body = {"input": [user_text,user_text2]};
            
            const response = await fetch('api/comparison', {
                            method: 'POST',
                            headers: {
                                'Content-Type': 'application/json'
                            },
                            body: JSON.stringify(body)
                            });
            const data  = await response.json();
            // data['Output'].forEach((val) => {arr.push(<li>{val}</li>)})
            set_text(data);
            setLoading(false);
            
            // console.log(document.getElementsByClassName('InnerContainer'));
            // console.log(document.getElementsByClassName('Output'));
            // document.getElementsByClassName('output').style.display='flex';
            // document.getElementsByClassName('Container').style.height='75%';
            // console.log(data['Output']);
        }
    else
        {set_text("Retry!")}
}

async function getsugg(user_change,setSuggestion){
    const body = {"name": user_change};
            
            const response = await fetch('api/suggestion', {
                            method: 'POST',
                            headers: {
                                'Content-Type': 'application/json'
                            },
                            body: JSON.stringify(body)
                            });
            const data  = await response.json();
            console.log(data);
            setSuggestion(data['suggestion']);
}

function Visulization() {
    const[text,set_text] = useState('');   
    const[text2,set_text2] = useState('');

    const[answer, setAnswer] = useState(' ');
    const[suggestion, setSuggestion] = useState([]);
    const[loading, setLoading] = useState(false);
    const[vis,set_vis] = useState(true);
    const [potta,set_potta] = useState('30%')
    const[visib,setVisib] = useState('visible')
    const handleSubmit = async  (e) => {
        e.preventDefault(); // Prevent default form submission behavior
        await Submit(text,text2,setAnswer,setLoading);
        set_vis(false);
        set_potta('100%');
        setVisib('visible');
        const rc = document.getElementsByClassName('Rightcontainer');
        // console.log(rc);
        rc[0].style.backgroundImage = `url(${img_bg})`;
        const cont = document.getElementsByClassName('Container');
        // console.log(rc);
        cont[0].style.backgroundColor = 'rgba(100,99,99,0.6)';
        cont[0].style.top = '50%';
    }
    

    return (
        <div className='Container' style={{height:potta}}>
            <div className='InnerContainer' style={{visibility:visib}}>
                <h1>Player Comparison</h1>
            </div>
            <div className="search-container">
                <form action=""  method="get" className="forms" onSubmit={handleSubmit} >
                    <input type="text" placeholder="Search..." className="search" value={text} onChange={(e)=>{set_text(e.target.value);getsugg(e.target.value,setSuggestion);}} list="suggestions" style={{width: '312px' }}/>
                    <datalist id="suggestions">
                        {suggestion.map((item, index) => (
                            <option key={index} value={item}>
                                {item}
                            </option>
                        ))}
                    </datalist>
                    <input type="text" placeholder="Search..." className="search" value={text2} onChange={(e)=>{set_text2(e.target.value);getsugg(e.target.value,setSuggestion);}} list="suggestions" style={{width: '312px' }}/>
                    <datalist id="suggestions">
                        {suggestion.map((item, index) => (
                            <option key={index} value={item}>
                                {item}
                            </option>
                        ))}
                    </datalist>                    
                    <button type="submit" value='submit' ><i className="fa fa-search"></i></button>
                </form>
                </div>
                <div className='Inner_Container' style={{height:{potta}}}>
                {loading ? (
                    <div class="loading-circle"></div>
                                          // Show loading message or video
                ) : (
                    <Output answer={answer} vis={vis} compare={true}/>  // Show answer when not loading
                )}
            </div>
        </div>
    );
}

export default Visulization;