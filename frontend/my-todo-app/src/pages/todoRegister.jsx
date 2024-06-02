import { useState } from "react"
import { useNavigate } from "react-router-dom"
import { userLoginState } from "../state/userLoginState";
import axios from "axios";
import { apiEndpoint } from "../api/api";
import { useRecoilValue } from "recoil";


export const TodoRegister = () => {
    const navigate = useNavigate();
    const loginState = useRecoilValue(userLoginState);
    const [todoTitle, setTodoTitle] = useState('');
    const [todoDate, setTodoDate] = useState('');
    const [todoBudget, setTodoBudget] = useState(0);
    const [tasks, setTasks] = useState([{title: '', targetDate: '',}]);
    const [errorMessage, setErrorMessage] = useState('');

    const handleAddTask = () => {
        setTasks([...tasks, { title: '', targetDate: ''}]);
    };

    const handleTaskChange = (index, field, value) => {
        const newTasks = tasks.map((task, i) => i === index ? { ...task, [field]: value } : task);
        setTasks(newTasks);
    }

    const handleSubmit = async () => {
        if (!todoTitle || !todoDate || !todoBudget) {
            setErrorMessage('すべての項目を入力してください')
        }
        try {
            const todoData = {
                userId: loginState,
                title: todoTitle,
                targetDate: todoDate,
                budget: todoBudget,
                completed: false,
                tasks: tasks.map(task => ({
                    title: task.title,
                    targetDate: task.targetDate,
                    completed: false
                }))
            };
            console.log(todoData)
            await axios.post(`${apiEndpoint}/todo/register`,
                todoData,
                {
                headers: {
                    'Content-Type': 'application/json'
                    }
                }
            );
            alert('やりたいことが登録されました');
            navigate('/main');
        } catch (error) {
            console.error("Error registering todo:", error);
            alert('やりたいことの登録に失敗しました');
        }
    };

    return (
        <div className="flex flex-col items-center min-h-screen bg-black">
            <header className="absolute top-2 left-2">
                <button className="m-4 p-2 w-20 bg-gray" onClick={() => navigate('/main')}>戻る</button>
            </header>
            <h1 className="mt-8 mb-16 text-white text-4xl">やりたいこと登録</h1>
            <div className="flex flex-col items-center">
                <div className="justify-between p-2 m-2 w-full h-30 space-x-4">
                    <input 
                        type="text" 
                        placeholder="やりたいこと入力" 
                        value={todoTitle}
                        onChange={(e) => setTodoTitle(e.target.value)}
                        className="text-center h-12 w-60 mb-2"/>
                    <input 
                        type="date" 
                        placeholder="日時"
                        value={todoDate}
                        onChange={(e) => setTodoDate(e.target.value)}
                        className="pl-2 pr-2 text-center h-12"/>
                    <input 
                        type="number" 
                        placeholder="予算（万円）" 
                        value={todoBudget}
                        onChange={(e) => setTodoBudget(e.target.value)}
                        className="text-center h-12 w-30"/>
                </div>
                <h2 className="m-4 p-2 text-2xl text-white">中間目標</h2>
                {tasks.map((task, index) => (
                    <div key={index} className="justify-between p-2 mb-4 bg-white">
                        <input 
                            type="text" 
                            placeholder="やるべきこと入力" 
                            value={task.title}
                            onChange={(e) => handleTaskChange(index, 'title', e.target.value)}
                            className="text-center p-2"/>
                        <input 
                            type="date" 
                            placeholder="日時" 
                            value={task.targetDate}
                            onChange={(e) => handleTaskChange(index, 'targetDate', e.target.value)}
                            className="text-center"/>
                    </div>
                ))}
                <button className="m-2 p-2 bg-gray" onClick={handleAddTask}>追加</button>
            </div>
            {errorMessage && <p className="text-red mt-2">{errorMessage}</p>}
            <button className="mt-4 p-2 bg-btn_green w-40" onClick={handleSubmit}>登録</button>
        </div>
    )
} 