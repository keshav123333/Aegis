import {useState} from 'react'
import axios from 'axios'
import {useNavigate} from 'react-router-dom'
function Login(){
    const [username, setUsername] = useState('')
    const [password, setPassword] = useState('')
    const navigate = useNavigate()

const handleSubmit = async (e) => {
    
    // Handle login logic here
    const da={username:username,password:password}

    try {
        const response = await axios.post('https://crispy-space-acorn-jj59jvrp5wxqhp69r-8000.app.github.dev/login', da,{
    withCredentials: true
  })
        localStorage.setItem('token', response.data)
        console.log(response.data)
        navigate('/dashboard')
    } catch (error) {
        console.error('Login failed:', error)
    }
}

    


    

    return (
        <div>
            <h1>Login Page</h1>
            
                <label htmlFor="username">Username:</label>
                <input type="text" id="username" name="username" value={username} onChange={(e) => setUsername(e.target.value)} />
                <label htmlFor="password">Password:</label>
                <input type="password" id="password" name="password" value={password} onChange={(e) => setPassword(e.target.value)} />
                <button type="submit" onClick={handleSubmit}>Login</button>
            
        </div>
    )
}

export default Login