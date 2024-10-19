import './Layout.css'
import {Outlet, Link} from 'react-router-dom';
import Logo from './assets/img/cricket.png';
import QA from './assets/img/QA.png'
import Book from './assets/img/book.png';
import Comparison from './assets/img/versus.png';
function Layout() {
    return (
        <div className='MainContainer'>
                <div className='Leftcontainer'>
                    <div className='innerleft'>
                        <div className='logo_name'>
                            <img src={Logo} className='Logo'></img>
                            <h2>O D I</h2>
                        </div>
                        <div className='list_link'>
                            <Link to='/Analysis'>
                            <div className='link_logo'>
                                <img src={QA} className='Comparison'/>
                                Q&A
                            </div>
                            </Link>
                            <Link to='/Rules'>
                            <div className='link_logo'>
                                <img src={QA} className='Comparison'/>
                                AUDIO
                            </div>
                            </Link>
                            <Link to='/Visualization'>
                            <div className='link_logo'>
                                <img src={Comparison} className='Comparison'/>
                                Comparison
                            </div>
                            </Link>
                        </div>
                        <div className='condition'>
                            <h2>Please provide either First/Last name of the players</h2>
                        </div>
                    </div>
                </div>
                <div className='Rightcontainer'>
                    <Outlet/>
                </div>
        
        </div>
        );
}

export default Layout;