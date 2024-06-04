import { useEffect, useState } from "react"
import axios from "axios"
import { useNavigate } from "react-router-dom"
import { apiEndpoint } from "../api/api"
import { useRecoilState } from "recoil"
import { userLoginState } from "../state/userLoginState"

export const Main = () => {
    const navigate = useNavigate();
    const [loginState, setLoginState] = useRecoilState(userLoginState);
    const [userInfo, setUserInfo] = useState({});

    useEffect(() => {
        const fetchUserInfo = async () => {
            try {
                console.log('userId:', loginState);
                const response = await axios.get(`${apiEndpoint}/api/user/info`, {
                    params: {
                        userId: loginState,
                    },
                });
                console.log('API response:', response.data);
                setUserInfo(response.data);
            } catch (error) {
            console.error("Error fetching user info:", error);
            }
        };
        
        if (loginState) {
            fetchUserInfo();
        }
    }, [loginState]);

    const handleLogout = () => {
        const isConfirmed = window.confirm('ログアウトしますか？');
        if (isConfirmed) {
            setLoginState('')
            navigate('/')
        }
    }

    const todoRender = () => {
        if (userInfo.todos) {
            return userInfo.todos.map((todo, index) => (
                <div key={index} className="p-4 bg-gray mb-4">
                    <h2 className="text-xl">{todo.Title}</h2>
                    <p>残り日数： {todo.RemainingDays}日</p>
                    <p>進捗： {todo.Progress}%</p>
                </div>
            ))
        }
    }

    return (
        <div className="flex flex-col items-center min-h-screen bg-cover" style={{ backgroundImage: `url('/items.png')` }}>
            <header className="flex justify-between w-full">
                <button className="h-10 m-4 p-2 bg-gray" onClick={handleLogout}>ログアウト</button>
                <div className="flex flex-col">
                    <h1 className="mt-4 p-2 bg-black text-white text-4xl">あなたの人生は残り</h1>
                    {userInfo.user && (
                        <h1 className="mb-4 p-2 text-center bg-black text-white text-4xl">
                            <span className="font-italic text-6xl text-red">{userInfo.user.RemainingLife.Years}</span>年と
                            <span className="font-italic text-6xl text-red">{userInfo.user.RemainingLife.Days}</span>日
                        </h1>
                    )}
                    
                </div>
                <button className="h-10 m-4 p-2 bg-gray" onClick={() => navigate('/user')}>プロフィール</button>
            </header>
            <div className="flex flex-col mt-10">
                {todoRender()}
            </div>
            <button className="m-4 p-2 w-20 bg-gray" onClick={() => navigate('/todoregister')}>追加</button>
        </div>
    )
}