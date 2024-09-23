import React from 'react'
import './Output.css';
// import Orginal from './img/Sachin Tendulkar.png';
// import Removed from './img/Virat Kohli.png';
// import image1 from './assets/images/image1.png';
// import image2 from './assets/images/image2.png';

function Output(props) {
    console.log(props);
    if(props.compare){
                    
        if(props.vis){
            return (
            <div className='Output' style={{visibility:'hidden'}}>
                
            </div>
            )}
        else{
            return (
            <div className='Output' style={{visibility:'visible'}}>
                <div className='Output1' >
                    <div className='Player_info1'>
                        <img src = {`data:image/png;base64,${props.answer.img1}`}  className='Compare_img1'/>
                    </div>
                </div>
                <div class='Middle_info'>
                    <div class="center-box">
                        
                        <div class="stats-table">
                            <div class="row">
                                <div class="player_name_left">{props.answer.image1[0]}</div>
                                <div class="player_stat_box">INNINGS</div>
                                <div class="player_name_right">{props.answer.image2[0]}</div>
                            </div>
                            <div class="divider"></div> 

                            <div class="row">
                                <div class="player_name_left">{props.answer.image1[1]}</div>
                                <div class="player_stat_box">RUNS</div>
                                <div class="player_name_right">{props.answer.image2[1]}</div>
                            </div>
                            <div class="divider"></div> 

                            <div class="row">
                                <div class="player_name_left">{props.answer.image1[2]}</div>
                                <div class="player_stat_box">AVERAGE</div>
                                <div class="player_name_right">{props.answer.image2[2]}</div>
                            </div>
                            <div class="divider"></div> 

                            <div class="row">
                                <div class="player_name_left">{props.answer.image1[3]}</div>
                                <div class="player_stat_box">FIFTIES</div>
                                <div class="player_name_right">{props.answer.image2[3]}</div>
                            </div>
                            <div class="divider"></div> 

                            <div class="row">
                                <div class="player_name_left">{props.answer.image1[4]}</div>
                                <div class="player_stat_box">CENTURIES</div>
                                <div class="player_name_right">{props.answer.image2[4]}</div>
                            </div>
                            <div class="divider"></div> 

                            <div class="row">
                                <div class="player_name_left">{props.answer.image1[5]}</div>
                                <div class="player_stat_box">FOURS</div>
                                <div class="player_name_right">{props.answer.image2[5]}</div>
                            </div>
                            <div class="divider"></div> 

                            <div class="row">
                                <div class="player_name_left">{props.answer.image1[6]}</div>
                                <div class="player_stat_box">SIXES</div>
                                <div class="player_name_right">{props.answer.image2[6]}</div>
                            </div>
                        </div>
                    </div>

                </div>
                <div className='Output2'>
                     <div className='Player_info2'>
                        <img src = {`data:image/png;base64,${props.answer.img2}`} className='Compare_img2'/>
                     </div>
                </div>
            </div>
       
            )
        }
    }

    else{
        
        if(props.vis){
            return (
            <div className='output' style={{visibility:'hidden'}}>{props.answer}</div>
            )}
        else{
            return (
            <div className='output' style={{visibility:'visible'}}>{props.answer}</div>
            )
        }
    }

}

export default Output;
