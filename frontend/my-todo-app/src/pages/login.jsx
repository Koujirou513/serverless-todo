import { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import { apiEndpoint } from '../api/api';
import { useSetRecoilState } from 'recoil';
import { userLoginState } from '../state/userLoginState';

export const Login = () => {
    const navigate = useNavigate();
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [errorMessage, setErrorMessage] = useState('');
    // atomへの更新関数を変数に入れる
    const setLogin = useSetRecoilState(userLoginState);

    const handleSignUpNavigate = () => {
        navigate('/signup');
    }

    const handleEmailChange = (e) => {
        setEmail(e.target.value);
    };

    const handlePasswordChange = (e) => {
        setPassword(e.target.value);
    };

    const handleLogin = async () => {
        if (!email || !password) {
            setErrorMessage('メールアドレスとパスワードを入力してください');
            return;
        }

        try {
            const response = await axios.post(`${apiEndpoint}/login`,{
                email,
                password
            }, {
                headers: {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*'
                }
            });
            // response.dataとuserIdがあるか判定
            if (response.data && response.data.userId) {
                // RecoilのatomにユーザーIDを保存
                setLogin(response.data.userId);
                // ログイン成功後にmainへリダイレクト
                navigate('/main');
            } else {
                setErrorMessage('ログインに失敗しました。');
            }
        } catch (error) {
            setErrorMessage('ログインに失敗しました')
        }
    }

    return (
        <div className="flex flex-col justify-center items-center min-h-screen" style={{backgroundImage: `url('src/assets/start.jpg')`}}>
            <title>死ぬまでにやりたいことリスト</title>
            <header className='absolute top-2 right-3 m-4'>
                <button className='bg-btn_green p-2'  onClick={(handleSignUpNavigate)}>新規登録</button>
            </header>
            <h1 className='text-4xl mb-8 text-gray'>死ぬまでにやりたいことリスト</h1>
            <div className='flex flex-col mt-8 w-80 items-center space-y-16'>
                <input 
                    type="email" 
                    placeholder="メールアドレス" 
                    value={email}
                    onChange={handleEmailChange}
                    className='p-2 text-center w-full' 
                />
                <input 
                    type="password" 
                    placeholder="パスワード" 
                    value={password}
                    onChange={handlePasswordChange}
                    className='p-2 text-center w-full'
                />
                <button onClick={handleLogin} className='p-2 bg-blue w-24'>
                    ログイン
                </button>
                {errorMessage && <p className='text-red mt-2'>{errorMessage}</p>}
            </div>
        </div>
    )
}
