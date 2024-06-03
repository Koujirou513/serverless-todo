import { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import { apiEndpoint } from '../api/api';
import { useSetRecoilState } from 'recoil';
import { userLoginState } from '../state/userLoginState';

export const SignUp = () => {
    const navigate = useNavigate();
    const [name, setName] = useState('');
    const [email, setEmail] = useState('');
    const [birthdate, setBirthdate] = useState('');
    const [gender, setGender] = useState('');
    const [password, setPassword] = useState('');
    const [confirmPass, setConfirmPass] = useState('');
    const [errorMessage, setErrorMessage] = useState('');
    const setLogin = useSetRecoilState(userLoginState)

    const handleLoginNavigate = () => {
        navigate('/');
    }

    const handleGenderClick = (selectedGender) => {
        setGender(selectedGender);
    }

    const handleSignUp = async () => {
        if (!name || !email || !birthdate || !gender || !password || !confirmPass) {
            setErrorMessage('全てのフィールドを入力してください');
            return;
        }

        if (password !== confirmPass) {
            setErrorMessage('パスワードが一致しません');
            return;
        }
        
        try {
            const response = await axios.post(`${apiEndpoint}/api/user/register`, {
                name,
                email,
                birthdate,
                gender,
                password
            }, {
                headers: {
                    'Content-Type': 'application/json'
                }
            });

            if (response.data && response.data.userId) {
                console.log(response.data)
                setLogin(response.data.userId);
                navigate('/main');
            } else {
                setErrorMessage('登録に失敗しました');
            }
        } catch (error) {
            setErrorMessage('登録に失敗しました');
        }
    }

    

    return (
        <div className="flex flex-col justify-center items-center min-h-screen bg-no-repeat bg-cover" style={{backgroundImage: `url('src/assets/start.jpg')`}}>
            <header className='absolute top-2 left-3 m-4'>
                <button className="bg-gray p-2 w-16" onClick={handleLoginNavigate}>戻る</button>
            </header>
            <h1 className='text-4xl mb-8 text-title-gray'>死ぬまでにやりたいことリスト</h1>
            <div className="flex flex-col items-center space-y-6 mt-8 w-80">
                <input 
                    type="text" 
                    placeholder="あなたの名前" 
                    className="text-center w-full p-2" 
                    value={name} 
                    onChange={(e) => setName(e.target.value)}
                />
                <input 
                    type="email" 
                    placeholder="メールアドレス" 
                    className="text-center w-full p-2"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                />
                <input 
                    type="date" 
                    placeholder="生年月日" 
                    className="text-center w-full p-2"
                    value={birthdate}
                    onChange={(e) => setBirthdate(e.target.value)}
                />
                <div className="flex justify-between w-full">
                    <button
                        className={`p-2 w-full mr-1 ${gender === 'male' ? 'bg-blue text-white' : 'bg-title-gray text-black'}`}
                        onClick={() => handleGenderClick('male')} 
                    >男性</button>
                    <button
                        className={`p-2 w-full ml-1 ${gender === 'female' ? 'bg-blue text-white' : 'bg-title-gray text-black'}`}
                        onClick={() => handleGenderClick('female')} 
                    >女性</button>
                </div>
                <input 
                    type="password" 
                    placeholder="パスワード" 
                    className="text-center w-full p-2"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                />
                <input 
                    type="password" 
                    placeholder="確認用パスワード" 
                    className="text-center w-full p-2"
                    value={confirmPass}
                    onChange={(e) => setConfirmPass(e.target.value)}
                />
                <button className="p-2 w-full bg-btn_green" onClick={handleSignUp}>登録する</button>
                {errorMessage && <p className='text-red text-sm mt-2'>{errorMessage}</p>}
            </div>

        </div>
    )
}