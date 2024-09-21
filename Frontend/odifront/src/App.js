import React from 'react';
import Layout from './Layout';
import { Routes,Route } from 'react-router-dom';
import Analysis from './Analysis';
import Visualization from './Visualization';
function App() {
  return(
    // Routes to various components Layout(home page),Story,Company,Bussiness,Innovovation,Careets
      <Routes>
          <Route path='/' element={<Layout />}>                        
          <Route path='Analysis' element={<Analysis />}/>
          <Route path='Visualization' element={<Visualization/>}/>
          </Route>
      </Routes>
    );
  }

export default App;