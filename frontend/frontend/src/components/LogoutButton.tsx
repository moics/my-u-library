import axios from 'axios';
import { useNavigate } from 'react-router-dom';

export default function LogoutButton() {
  const navigate = useNavigate();

  const handleLogout = async () => {
    try {
      await axios.post('/auth/logout/');
      // Clear frontend state
      document.cookie.split(';').forEach(cookie => {
      const [name] = cookie.trim().split('=');
    });

      navigate('/login');  // Redirect to login page
    } catch (error) {
      console.error('Logout failed:', error);
    }
  };



  return (
    <button onClick={handleLogout} className="logout-button">
      Logout
    </button>
  );
}