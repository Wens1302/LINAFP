import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Navbar from './components/Navbar';
import Dashboard from './pages/Dashboard';
import Teams from './pages/Teams';
import Players from './pages/Players';
import Matches from './pages/Matches';
import Standings from './pages/Standings';
import Stats from './pages/Stats';
import Articles from './pages/Articles';
import Login from './pages/Login';

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/login" element={<Login />} />
        <Route
          path="/*"
          element={
            <>
              <Navbar />
              <main>
                <Routes>
                  <Route path="/" element={<Dashboard />} />
                  <Route path="/teams" element={<Teams />} />
                  <Route path="/players" element={<Players />} />
                  <Route path="/matches" element={<Matches />} />
                  <Route path="/standings" element={<Standings />} />
                  <Route path="/stats" element={<Stats />} />
                  <Route path="/articles" element={<Articles />} />
                </Routes>
              </main>
            </>
          }
        />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
