export const Profile = () => {
    return (
        <div>
            <header>
                <button>戻る</button>
                <h1>プロフィール</h1>
            </header>
            <body>
                <div>
                    <p>あなたの名前: 山田たろう</p>
                    <button>編集</button>
                </div>
                <p>メールアドレス: example@gmail.com</p>
                <p>生年月日: 1986/4/1</p>
                <p>年齢: 37</p>
                <p>性別: 男性</p>
            </body>
            <div>
                <button>登録解除</button>
            </div>
        </div>
    )
}