import React, { useState, createContext } from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Sidebar from './components/Sidebar';
import Dashboard from './pages/Dashboard';
import Categories from './pages/Categories';
import Upload from './pages/Upload';
import Results from './pages/Results';

export const AppContext = createContext();

function App() {
  const [results, setResults] = useState(null);
  
  return (
    <AppContext.Provider value={{ results, setResults }}>
      <BrowserRouter>
        <div className="flex bg-background min-h-screen text-gray-100 font-sans">
          <Sidebar />
          <div className="flex-1 ml-64 p-8">
            <Routes>
              <Route path="/" element={<Dashboard />} />
              <Route path="/categories" element={<Categories />} />
              <Route path="/upload" element={<Upload />} />
              <Route path="/results" element={<Results />} />
            </Routes>
          </div>
        </div>
      </BrowserRouter>
    </AppContext.Provider>
  );
}

export default App;
