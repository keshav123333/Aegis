import {useState} from 'react'
import {useNavigate} from 'react-router-dom'
import axios from 'axios'
function Signup(){
    const navigate = useNavigate();
    const [username, setUsername] = useState('')
    const [email, setEmail] = useState('')
    const [community_saver, setCommunitySaver] = useState(false) 
    const [password, setPassword] = useState('')


const handleSubmit = async (e) => {
    
    // Handle signup logic here
    const da={username:username,password:password,email:email,community_saver:community_saver}

    try {
        const response = await axios.post('https://crispy-space-acorn-jj59jvrp5wxqhp69r-8000.app.github.dev/signup', da,{withCredentials: true})

        console.log(response.data)
        alert(response.data.message)
        navigate('/login') // Redirect to login page after successful signup

    } catch (error) {
        console.error('Signup failed:', error)
    }
}

    


    

    return (
        <div>
            <h1>Sign up</h1>
            
                <label htmlFor="username">Username:</label>
                <input type="text" id="username" name="username" value={username} onChange={(e) => setUsername(e.target.value)} />
                <label htmlFor="password">Password:</label>
                <input type="password" id="password" name="password" value={password} onChange={(e) => setPassword(e.target.value)} />
                <label htmlFor="email">Email:</label>
                <input type="email" id="email" name="email" value={email} onChange={(e) => setEmail(e.target.value)} />
                <label htmlFor="community_saver">Community Saver:</label>
                <input type="checkbox" id="community_saver" name="community_saver" checked={community_saver} onChange={(e) => setCommunitySaver(e.target.checked)} />
                <button type="submit" onClick={handleSubmit}>Signup</button>
            
            
        </div>
    )
}

export default Signup