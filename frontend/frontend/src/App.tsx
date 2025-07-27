import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import LoginForm from './LoginForm';
import BookTable from './BookTable';
import './App.css';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<LoginForm />} />
        <Route path="/books" element={<BookTable />} />
      </Routes>
    </Router>
  );
}

export default App;
