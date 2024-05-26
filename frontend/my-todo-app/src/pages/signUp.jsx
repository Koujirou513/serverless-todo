
export const SignUp = () => {


    return (
        <div>
            <header>
                <button>戻る</button>
            </header>
            <h1>死ぬまでにやりたいことリスト</h1>
            <body>
                <input type="text" placeholder="あなたの名前"/>
                <input type="email" placeholder="メールアドレス"/>
                <input type="date" placeholder="生年月日"/>
                <div>
                    <label><input type="radio" name="radio" value="male"/>男性</label>
                    <label><input type="radio" name="radio" value="female"/>女性</label>
                </div>
                <input type="password" placeholder="パスワード"/>
                <input type="password" placeholder="確認用パスワード"/>
                <button>登録する</button>
            </body>

        </div>
    )
}