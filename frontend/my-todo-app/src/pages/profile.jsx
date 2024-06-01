export const Profile = () => {
    return (
        <div className="flex flex-col justify-center items-center min-h-screen bg-no-repeat bg-cover" style={{backgroundImage: `url('src/assets/items.png')`}}>
            <header className="absolute top-2 left-2">
                <button className="m-4 p-2 w-20 bg-gray ">戻る</button>
            </header>
            <h1 className="mt-8 mb-16 text-4xl text-white">プロフィール</h1>

            <div>
                <div>
                    <p>あなたの名前: 山田たろう</p>
                    <button>編集</button>
                </div>
                <p>メールアドレス: example@gmail.com</p>
                <p>生年月日: 1986/4/1</p>
                <p>年齢: 37</p>
                <p>性別: 男性</p>
            </div>
            <div>
                <button>登録解除</button>
            </div>
        </div>
    )
}