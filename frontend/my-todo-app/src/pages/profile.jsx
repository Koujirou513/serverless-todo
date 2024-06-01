import { useEffect, useState } from "react"
import axios from "axios"
import { useNavigate } from "react-router-dom"
import { apiEndpoint } from "../api/api"
import { useRecoilState } from "recoil"
import { userLoginState } from "../state/userLoginState"

export const Profile = () => {
    const navigate = useNavigate();
    const [loginState, setLoginState] = useRecoilState(userLoginState);
    const [userProfile, setUserProfile] = useState({});
    const [isEditing, setIsEditing] = useState(false);
    const [newName, setNewName] = useState('');


    useEffect(() => {
        const fetchUserProfile = async () => {
            try {
                console.log('userId:', loginState);
                const response = await axios.get(`${apiEndpoint}/user/profile`, {
                    params: {
                        userId: loginState,
                    },
                });
                console.log('API response:', response.data);
                setUserProfile(response.data);
            } catch (error) {
            console.error("Error fetching user info:", error);
            }
        };
        
        if (loginState) {
            fetchUserProfile();
        }
    }, [loginState]);

    // 生年月日から年齢を計算する
    const calculateAge = (birthdate) => {
        const birthDate = new Date(birthdate);
        const today = new Date();
        let age = today.getFullYear() - birthDate.getFullYear();
        const monthDiff = today.getMonth() - birthDate.getMonth();
        if (monthDiff < 0 || (monthDiff === 0 && today.getDate() < birthDate.getDate())) {
            age--;
        }
        return age;
    }

    // 性別を日本語に変える関数
    const getGenderText = (gender) => {
        if (gender.toLowerCase() === 'male') {
            return '男性';
        } else if (gender.toLowerCase() === 'female') {
            return '女性';
        } else {
            return gender;
        }
    }

    // 編集モードかどうか判定する
    const handleEditClick = () => {
        setIsEditing(true);
    };

    // ユーザーの名前を変更する関数
    const handleSaveClick = async () => {
        try {
            await axios.patch(`${apiEndpoint}/user/update`, {
                userId: loginState,
                newName: newName,
            });
            setUserProfile((prevProfile) => ({
                ...prevProfile,
                user: {
                    ...prevProfile.user,
                    Name: newName,
                },
            }));
            setIsEditing(false);
        } catch (error) {
            console.error(error);
        }
    };

    // 新しい名前を入力
    const handleInputChange = (e) => {
        setNewName(e.target.value);
    };

    const handleDeleteUser = async () => {
        const isConfirmed = window.confirm('本当に登録解除しますか？');
        if (isConfirmed) {
            try {
                await axios.delete(`${apiEndpoint}/user/delete`, {
                    data: {
                        userId: loginState,
                    },
                });
                alert('ユーザーが削除されました');
                setLoginState('');
                navigate('/');
            } catch (error) {
                console.error('Error deleting user account:', error);
            }
        }
    }

    return (
        <div className="flex flex-col justify-center items-center min-h-screen bg-black">
            <header className="absolute top-2 left-2">
                <button className="m-4 p-2 w-20 bg-gray" onClick={() => navigate('/main')}>戻る</button>
            </header>
            <h1 className="mt-8 mb-16 text-4xl text-white">プロフィール</h1>

            <div className="p-8 flex flex-col items-center space-y-8">
                <div className='flex flex-row justify-center items-center'>
                    {isEditing ? (
                        <input
                            type="text"
                            value={newName}
                            placeholder={userProfile.user?.Name || ''}
                            onChange={handleInputChange}
                            className='text-center w-full p-2'
                        />
                    ) : (
                        <p className='text-white text-xl'>あなたの名前: {userProfile.user?.Name}</p>
                    )}
                    <button 
                        className='p-2 ml-8 bg-gray w-20'
                        onClick={isEditing ? handleSaveClick : handleEditClick}
                    >
                        {isEditing ? '保存' : '編集'}
                    </button>
                </div>
                <p className='text-white text-xl'>メールアドレス: {userProfile.user?.Email}</p>
                <p className='text-white text-xl'>生年月日: {userProfile.user?.Birthdate}</p>
                <p className='text-white text-xl'>年齢: {userProfile.user?.Birthdate ? calculateAge(userProfile.user.Birthdate) : ''}</p>
                <p className='text-white text-xl'>性別: {userProfile.user?.Gender ? getGenderText(userProfile.user.Gender) : ""}</p>
            </div>
            <div className='absolute bottom-4 right-4'>
                <button className='p-2 m-4 bg-gray' onClick={handleDeleteUser}>登録解除</button>
            </div>
        </div>
    )
}