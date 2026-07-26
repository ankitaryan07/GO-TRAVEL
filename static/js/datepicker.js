/* GO-TRAVEL Date Range Picker — check-in + check-out ek hi calendar me */

class DatePicker {
    constructor(containerId, onSelectCallback) {
        this.container = document.getElementById(containerId);
        this.onSelect = onSelectCallback;
        this.currentDate = new Date();
        this.checkIn = null;
        this.checkOut = null;
        this.render();
    }

    render() {
        this.container.innerHTML = `
            <div class="datepicker-modal">
                <div class="datepicker-header">
                    <h3>Select Dates</h3>
                    <button class="close-btn" onclick="window.currentPicker.close()">×</button>
                </div>
                <div class="datepicker-selection">
                    <div class="sel-box ${!this.checkOut ? 'active' : ''}">
                        <span class="sel-label">Check-in</span>
                        <span class="sel-val" id="selCheckIn">--</span>
                    </div>
                    <span style="font-size:20px;color:var(--orange);">→</span>
                    <div class="sel-box ${this.checkIn && !this.checkOut ? 'active' : ''}">
                        <span class="sel-label">Check-out</span>
                        <span class="sel-val" id="selCheckOut">--</span>
                    </div>
                </div>
                <div class="datepicker-body">
                    <div class="datepicker-controls">
                        <button onclick="window.currentPicker.prevMonth()" class="nav-btn">‹</button>
                        <h4 id="monthYear"></h4>
                        <button onclick="window.currentPicker.nextMonth()" class="nav-btn">›</button>
                    </div>
                    <div id="calendar" class="calendar"></div>
                    <p class="dp-hint" id="dpHint">Tap a date to set check-in</p>
                </div>
                <div class="datepicker-footer">
                    <button onclick="window.currentPicker.close()" class="btn-cancel">Cancel</button>
                    <button onclick="window.currentPicker.confirm()" class="btn-select">Confirm</button>
                </div>
            </div>`;
        window.currentPicker = this;
        this.renderCalendar();
    }

    renderCalendar() {
        const year = this.currentDate.getFullYear();
        const month = this.currentDate.getMonth();
        const monthNames = ["January","February","March","April","May","June",
                          "July","August","September","October","November","December"];
        document.getElementById('monthYear').textContent = `${monthNames[month]} ${year}`;

        let html = '<div class="calendar-grid">';
        ['Sun','Mon','Tue','Wed','Thu','Fri','Sat'].forEach(d => html += `<div class="day-header">${d}</div>`);

        const firstDay = new Date(year, month, 1).getDay();
        const daysInMonth = new Date(year, month + 1, 0).getDate();
        const today = new Date(); today.setHours(0,0,0,0);

        for (let i = 0; i < firstDay; i++) html += '<div class="day empty"></div>';

        for (let day = 1; day <= daysInMonth; day++) {
            const dateStr = `${year}-${String(month+1).padStart(2,'0')}-${String(day).padStart(2,'0')}`;
            const date = new Date(year, month, day);
            const isPast = date < today;
            let cls = "day";
            if (isPast) cls += " disabled";
            if (dateStr === this.checkIn) cls += " range-start";
            if (dateStr === this.checkOut) cls += " range-end";
            if (this.checkIn && this.checkOut && dateStr > this.checkIn && dateStr < this.checkOut)
                cls += " in-range";
            html += `<div class="${cls}" onclick="window.currentPicker.pick('${dateStr}', ${isPast})">${day}</div>`;
        }
        html += '</div>';
        document.getElementById('calendar').innerHTML = html;

        document.getElementById('selCheckIn').textContent = this.checkIn || "--";
        document.getElementById('selCheckOut').textContent = this.checkOut || "--";
        const hint = document.getElementById('dpHint');
        if (!this.checkIn) hint.textContent = "Tap a date to set check-in";
        else if (!this.checkOut) hint.textContent = "Now tap a date for check-out";
        else hint.textContent = "Dates selected! Tap Confirm.";
    }

    pick(dateStr, isPast) {
        if (isPast) return;
        if (!this.checkIn || (this.checkIn && this.checkOut)) {
            // naya selection start
            this.checkIn = dateStr;
            this.checkOut = null;
        } else {
            // check-out — must be after check-in
            if (dateStr <= this.checkIn) {
                this.checkIn = dateStr;  // agar pehle ka click kiya to reset check-in
                this.checkOut = null;
            } else {
                this.checkOut = dateStr;
            }
        }
        this.renderCalendar();
    }

    confirm() {
        if (this.checkIn && this.checkOut) {
            this.onSelect(this.checkIn, this.checkOut);
            this.close();
        } else {
            alert("Please select both check-in and check-out dates");
        }
    }

    prevMonth() { this.currentDate.setMonth(this.currentDate.getMonth()-1); this.renderCalendar(); }
    nextMonth() { this.currentDate.setMonth(this.currentDate.getMonth()+1); this.renderCalendar(); }
    close() { this.container.remove(); }
}

function openDatePicker(callback) {
    const old = document.getElementById('datepicker-container');
    if (old) old.remove();
    const container = document.createElement('div');
    container.id = 'datepicker-container';
    document.body.appendChild(container);
    new DatePicker('datepicker-container', callback);
}
