import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import { Login } from "../pages/login";
import { SignUp } from "../pages/signUp";
import { Main } from "../pages/main";
import { Profile } from "../pages/profile";
import { TodoDetail } from "../pages/todoDetail";
import { TodoRegister } from "../pages/todoRegister";

export const AppRouter = () => {
    return (
        <Router>
            <Routes>
                <Route path='/' element={<Login />} />
                <Route path='/signup' element={<SignUp />} />
                <Route path='/main' element={<Main />} />
                <Route path='/user' element={<Profile />} />
                <Route path='/todo' element={<TodoDetail />} />
                <Route path='/todoregister' element={<TodoRegister />} />
            </Routes>
        </Router>
    )
}