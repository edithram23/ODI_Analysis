import React from 'react';
import Layout from './Layout';
import { Routes,Route,Navigate  } from 'react-router-dom';
import Analysis from './Analysis';
import Visualization from './Visualization';
import Rules from './Rules';
function App() {
  return(
    // Routes to various components Layout(home page),Story,Company,Bussiness,Innovovation,Careets
      <Routes>
          <Route path='/' element={<Layout />}>    
          <Route index element={<Navigate to="/Rules" replace />} />                    
          <Route path='Analysis' element={<Analysis />}/>
          <Route path='Visualization' element={<Visualization/>}/>
          <Route path='Rules' element={<Rules/>}/>
          </Route>
      </Routes>
    );
  }

export default App;