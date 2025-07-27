import { useForm } from 'react-hook-form';
import axios from 'axios';

import { useNavigate } from 'react-router-dom';

type FormData = {
  username: string;
  password: string;
};

export default function LoginForm() {
  const { register, handleSubmit, formState: { errors } } = useForm<FormData>();
  
  const navigate = useNavigate();

  const onSubmit = async (data: FormData) => {
    try {
      const response = await axios.post(
        'http://localhost:8000/api/auth/login/', 
        data,
        { 
          withCredentials: true
        }
      );
      
      //console.log('Login successful:', response.data);
      navigate('/books/');

    } catch (error) {
      //console.error('Login failed:', error.response?.data);
    }
  };

  

  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      <div>
        <label>Username</label>
        <input 
          {...register('username', { required: 'Username required' })} 
          type="text"
        />
        {errors.username && <p>{errors.username.message}</p>}
      </div>

      <div>
        <label>Password</label>
        <input 
          {...register('password', { required: 'Password required' })} 
          type="password"
        />
        {errors.password && <p>{errors.password.message}</p>}
      </div>

      <button type="submit">Login</button>
    </form>
  );
}