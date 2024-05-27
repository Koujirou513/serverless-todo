export const TodoRegister = () => {
    return (
        <div>
            <header>
                <button>戻る</button>
                <h1>やりたいこと登録</h1>
            </header>
            <body>
                <div>
                    <input type="text" placeholder="やりたいこと入力" />
                    <input type="date" placeholder="日時" />
                    <input type="number" placeholder="予算" />
                </div>
                <h2>中間目標</h2>
                <div>
                    <div>
                        <input type="text" placeholder="やるべきこと入力" />
                        <input type="date" placeholder="日時" />
                    </div>
                </div>
                <button>追加</button>
            </body>
            <button>登録</button>
        </div>
    )
} 