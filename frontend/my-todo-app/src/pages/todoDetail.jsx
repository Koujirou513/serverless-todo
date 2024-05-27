export const TodoDetail = () => {
    return (
        <div>
            <header>
                <button>戻る</button>
                <h1>やりたいこと詳細</h1>
            </header>
            <body>
                <div>
                    <button>未</button>
                    <input type="text" placeholder="富士山に登る"/>
                    <input type="date" placeholder="2025/5/15" />
                    <input type="text" placeholder="予算: 50万円" />
                    <button>削除</button>
                </div>
                <div>
                    <h2>中間目標</h2>
                    <div>
                        <button>未</button> 
                        <input type="text" placeholder="1000メートル以上の山を登る"/>
                        <input type="date" placeholder="2025/4/15" />
                        <button>削除</button>
                    </div>
                </div>
                <button>追加</button>
                <button>変更を保存</button>
            </body>
        </div>
    )
}