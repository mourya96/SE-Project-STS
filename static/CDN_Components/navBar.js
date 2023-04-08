const navBar = {
    template: `
    <div>
        <h1 class="text-center m-3">{{title}}</h1>
        <div class="position-relative" style="margin-left: 3%; margin-right: 3%;">
            <h3 class=" ms-3">Welcome {{username}}</h3>
            <div class="text-end me-1 position-absolute top-0 end-0">
                <button @click="logout" style="font-size: large;" class="btn btn-info">
                    Logout <i class="bi bi-box-arrow-right"></i>
                </button>
            </div>
            <hr class="border border-primary border-2 opacity-100">
        </div>
    </div>`,
    data() {
        return {
            username: 'student'
        }
    },
    props: ["title"],
    methods: {
        logout() {
            alert("Logout Successfully")
            localStorage.clear()
        }
    },
}
export default navBar