// import React, { useState } from 'react';
// import axios from 'axios';
// import { useNavigate } from 'react-router-dom';
// import { apiEndpoint } from '../../api/api';
// import { useSetRecoilState } from 'recoil';
// import { userLoginState } from '../../state/userLoginState';

export const Login = () => {
    // const navigate = useNavigate();
    // const [email, setEmail] = useState('');
    // const [password, setPassword] = useState('');
    // const [errorMessage, setErrorMessage] = userState('');
    // // atomへの更新関数を変数に入れる
    // const setLogin = useSetRecoilState(userLoginState);
    

    return (
        <div>
            <header>
            <title>死ぬまでにやりたいことリスト</title>
                <button>新規登録</button>
            </header>
            <h1>死ぬまでにやりたいことリスト</h1>
            <body>
                <input type="email" placeholder="メールアドレス"/>
                <input type="password" placeholder="パスワード" />
                <button>ログイン</button>
            </body>
        </div>
    )

}
